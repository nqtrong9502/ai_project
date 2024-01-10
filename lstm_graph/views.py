from django.shortcuts import render
import os
from django.http import HttpResponse
from django.views.generic import View

from urllib.parse import urlparse

class MyViewLSTMGRAPH(View):
  def get(self, request, *args, **kwargs):
    # ga = [1,2,3]
    print(123)
    return render(request, f"lstmgraph.html")
  def post(self, request, *args, **kwargs):

    pass

