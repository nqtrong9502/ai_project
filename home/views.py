from django.shortcuts import render
import os
from django.http import HttpResponse
from django.views.generic import View

from urllib.parse import urlparse


def get_domain_name(url):
    domain = urlparse(url).netloc
    return domain

class MyViewHome(View):
  def get(self, request, *args, **kwargs):
    ga = [1,2,3]
    return render(request, f"home.html", {'ga':ga})
  def post(self, request, *args, **kwargs):

    pass

