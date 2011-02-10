import urllib2
from pyquery import PyQuery as pq
import re
import time
from lxml import etree
from django.core.management.base import NoArgsCommand
from reps.models import *


class Command(NoArgsCommand):
    """command for loading bills directly from the azleg website"""
    # wait time for each document. Robots.txt on their website requests it. I ignore their ignore patterns,
    # because it's public data, and I want the bills, but lets not kill their servers spidering and *really* annoy someone
    speed_limit = 5
    # speed_limit = 120 
    
    def handle_noargs(self, **options):        
        d = pq(urllib2.urlopen('http://www.azleg.gov/Bills.asp').read())
        hbs = {
            'start' : None,
            'end' : None,
        }
        sbs = {
            'start' : None,
            'end' : None,
        }
        for link in d("table.ContentAreaBackground a"):
            # calculate start and end ids for house and senate bills by looking at the left hand nav
            value = link.values()[0]
            s = re.search(r"FirstBill\=(?P<start_id>(HB|SB)\d+).*\&LastBill\=(?P<end_id>(HB|SB)\d+)", value)
            if s:
                ids = s.groupdict()
                if ids['start_id'][0:2] == "HB":
                    if ids['start_id'][2:] < hbs['start'] or not hbs['start']:
                        hbs['start'] = ids['start_id'][2:]
                if ids['start_id'][0:2] == "HB":
                    if ids['end_id'][2:] > hbs['end'] or not hbs['end']:
                        hbs['end'] = ids['end_id'][2:]
                if ids['start_id'][0:2] == "SB":
                    if ids['start_id'][2:] < sbs['start'] or not sbs['start']:
                        sbs['start'] = ids['start_id'][2:]
                if ids['start_id'][0:2] == "SB":
                    if ids['end_id'][2:] > sbs['end'] or not sbs['end']:
                        sbs['end'] = ids['end_id'][2:]
        for hbno in range(int(hbs['start']), int(hbs['end']) + 1):
            self.process_bill("HB%s" % (hbno))
        for sbno in range(int(sbs['start']), int(sbs['end']) + 1):
            self.process_bill("SB%s" % (sbno))
        
    
    def process_bill(self, bill_name):
        """get and process a bill"""
        print "waiting %d seconds to fetch %s" % (self.speed_limit, bill_name)
        time.sleep(self.speed_limit)
        d = pq(urllib2.urlopen('http://www.azleg.gov/DocumentsForBill.asp?Bill_Number=%s' % (bill_name)).read())
        bill, created = Bill.objects.get_or_create(pk=bill_name)
        bill.short_title = d('.ContentPageTitle').text() # amalgamate the text of all ContentPageTitle elements.
        bill.save()
        # find bill overview link
        overviewitem = d('.TableHeaderBackground')[0].getnext()
        self.process_documents_row('Show Overview', bill, overviewitem)
        # find "show" links
        links = d(".InactiveItem")
        items = d("div.BillsLayer")
        titles = []
        count = 0
        for link in links:
            self.process_documents_row(link.text, bill, items[count])
            count = count + 1
    
    def process_documents_row(self, title, bill, item):
        """process a row from the DocumentsForBill.asp page"""
        # first, find the documents. Documents are passed through "formatdocument.asp" to add site formatting. We can get
        # rid of that extraneous information by going straight to the root document.  We'll ignore PDF docs for the moment.
        links = item.cssselect('a')
        for link in links:
            if link.attrib['href'][:46] == 'http://www.azleg.gov/FormatDocument.asp?inDoc=':
                # we have a link to an html document, add it to documents list.
                try:
                    docpath = urllib2.unquote(link.attrib['href'][46:])
                    documenturl = "http://www.azleg.gov%s" % (docpath)
                    document, created = BillDocument.objects.get_or_create(pk=documenturl, defaults={'bill':bill})
                    if created or document.type == 'Overview':
                        # fetch newly created documents, always refetch overviews
                        print "waiting %d seconds to fetch %s" % (self.speed_limit, docpath)
                        time.sleep(self.speed_limit)
                        document.document = unicode(urllib2.urlopen(documenturl).read(), 'windows-1252').encode('utf-8')
                        document.title = self.tr_link_text_sanitizer(link).encode('utf-8')
                        document.type = ' '.join(title.split()[1:]) # remove the show
                        document.bill = bill
                        document.save()
                    else:
                        print "skipping %s, because we already have a copy" % (docpath) # skip this while we're building crawler                    
                except Exception, e:
                    print e
                
        if title == "Show Sponsors":
            # deal with sponsors
            for link in links:
                r = re.search('Member_ID=(?P<member_id>\d+)&legislature=(?P<legislature_id>\d+)&Session=(?P<session_id>.*)$', link.attrib['href'])
                representative, createdrep = Representative.objects.get_or_create(azleg_id=r.groupdict()['member_id'])
                sponstype = link.getparent().getnext().text_content()
                sponsorship, created = Sponsorship.objects.get_or_create(representative=representative, bill=bill, defaults={'type' : str(sponstype)})
        #elif title == u'\xa0Show Versions':
        #    # deal with bill versions
        #    pass
        #elif title == 'Show Summaries/Fact Sheets':
        #    # deal with fact sheets
        #    pass
        #elif title == 'Show Adopted Amendments' or title == 'Show Proposed Amendments':
        #    # deal with amendments
        #    if title == 'Show Adopted Amendments':
        #        adopted = True
        #    else:
        #        adopted = False
        #elif title == 'Show Fiscal Notes':
        #    # deal with fiscal notes
        #    pass
        #elif title == 'Show House Agendas' or title == 'Show Senate Agendas':
        #    # deal with agenda
        #    pass
            
    def tr_link_text_sanitizer(self, link):
        """sanitize the link text"""
        # this is *VERY* rough for the moment. We WILL have to clean this up later
        # at the moment, if the name of a document has "Click" in it, we'll be in trouble
        rubbish_names = ['HTML', 'PDF', 'Click']
        parent = link.getparent()
        textsplits = parent.text_content().split()
        while textsplits[0] in rubbish_names:
            parent = parent.getparent() # recurse up the DOM
            textsplits = parent.text_content().split()
        name = ''
        for word in textsplits:
            if word in rubbish_names:
                break
            else:
                name = name + ' ' + word
        return name