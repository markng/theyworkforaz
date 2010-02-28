import urllib2
from pyquery import PyQuery as pq
import re
from lxml import etree
from django.core.management.base import NoArgsCommand
from reps.models import *

class Command(NoArgsCommand):
    """command for loading house members directly from the azleg website"""
    def handle_noargs(self, **options):        
        d = pq(urllib2.urlopen('http://www.azleg.gov/MemberRoster.asp?Body=H').read())
        table = d('#house')
        reprows = table.children()[1:]
        h, created = House.objects.get_or_create(name="House", code='H')
        self.processrows(reprows, h)
        d = pq(urllib2.urlopen('http://www.azleg.gov/MemberRoster.asp?Body=S').read())
        table = d('#senate')
        reprows = table.children()[1:]
        s, created = House.objects.get_or_create(name="Senate", code='S')
        self.processrows(reprows, s)
        
    def processrows(self, reprows, house):
        """process rows from page"""
        find_member_id = re.compile('Member_ID=(?P<member>.*?)&Legislature')
        reps = []
        for reprow in reprows:
            cells = reprow.getchildren()
            rep = {}
            namesplit = cells[0].text_content().strip().partition('\r')
            rep['name'] = namesplit[0]
            if len(namesplit) > 1:
                rep['role'] = namesplit[2].strip()
            rep['district'] = cells[1].text_content().strip()
            rep['party'] = cells[2].text_content().strip()
            rep['email'] = cells[3].text_content().strip()
            rep['room'] = cells[4].text_content().strip()
            rep['phone'] = "602-%s" % (cells[5].text_content().strip())
            rep['fax'] = "602-%s" % (cells[6].text_content().strip())
            if cells[0].getchildren()[0].values()[0] == 'vacantmember':
                rep['current'] = False
                link = cells[0].getchildren()[0].values()[1]
            else:
                rep['current'] = True
                link = cells[0].getchildren()[0].values()[0]
            rep['link'] = "http://www.azleg.gov%s" % (link)
            rep['id'] = find_member_id.search(link).groupdict()['member']
            rep['house'] = house
            self.add_member(rep)
    
    def add_member(self, rep):
        """add a member from a parsed row"""
        party, created = Party.objects.get_or_create(code = rep['party'])
        defaults = {
            'party' : party,
            'name' : rep['name'],
        }
        r, created = Representative.objects.get_or_create(id=rep['id'], defaults=defaults)
        r.name = rep['name']
        r.role = rep['role']
        r.district = District.objects.get(id=rep['district'])
        r.party = party
        r.email = rep['email']
        r.room = rep['room']
        r.phone = rep['phone']
        r.fax = rep['fax']
        r.current = rep['current']
        r.link = rep['link']
        r.house = rep['house']
        r.save()
        