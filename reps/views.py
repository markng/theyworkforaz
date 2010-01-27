from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from forms import WhereForm

def home(request):
    """home page"""
    if request.method == 'POST':
        form = WhereForm(request.POST)
        if form.is_valid():
            district = 9
            return HttpResponseRedirect('/district/%s' % (district))
    else:
        form = WhereForm()

    return render_to_response('index.html', { 'form' : form, })