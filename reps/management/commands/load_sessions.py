import urllib2
from django.core.management.base import NoArgsCommand
from reps.models import Session
from pyquery import PyQuery as pq

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        sessions = pq(urllib2.urlopen('http://azleg.gov/xml/sessions.asp?sort=SessionID').read())
        sessionrow = [session.attrib for session in sessions.children()]     
        for session in sessionrow:
            s, created = Session.objects.get_or_create(id=session['Session_ID'])
            s.from_session_dict(session)