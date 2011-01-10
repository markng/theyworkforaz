import urllib2
from pyquery import PyQuery as pq
import re
import time
from lxml import etree
from django.core.management.base import NoArgsCommand
from reps.models import *


class Command(NoArgsCommand):
    """command for loading votes and actions directly from the azleg website"""
    def handle_noargs(self, **options):
        # work out which bills we need to load actions from
        bills = Bill.objects.all()
        for bill in bills:
            pass