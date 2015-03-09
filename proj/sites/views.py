from django.shortcuts import render

from django.contrib.auth.decorators import login_required

@login_required(login_url = '/account/login/')
def index(request):
    from sites.models import Site
    sites = Site.objects.filter(user=user)

