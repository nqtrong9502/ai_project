from django.shortcuts import render
import joblib
import numpy as np
# Create your views here.
from django import forms


  
from django.http import HttpResponse
from django.views.generic import View

def gaussian_membership_function(x, mean, sigma):
  exponent = -np.power((x - mean) / sigma, 2) / 2
  # Calculate the membership value.
  membership = np.exp(exponent)

  return membership
mean_age, std_age = 31.705, 12.12385974019825
mean_fre, std_fre = 2.365, 1.6738503517339893
mean_visual,std_visual = 1.4875, 0.9898705723477187

class MyViewHeadachePrediction(View):
  def get(self, request, *args, **kwargs):
    return render(request,"index.html")
  def post(self, request, *args, **kwargs):
    method = None
    if request.method == "POST":
      age = int(request.POST['age'])
      age = gaussian_membership_function(age, mean_age,std_age)
      duration = int(request.POST['duration'])
      frequency = int(request.POST['frequency'])
      frequency = gaussian_membership_function(frequency, mean_fre,std_fre)

      location = int(request.POST['location'])
      character = int(request.POST['character'])
      intensity = int(request.POST['intensity'])
      nausea = int(request.POST['nausea'])
      vomit = int(request.POST['vomit'])
      phonophobia = int(request.POST['phonophobia'])
      photophobia = int(request.POST['photophobia'])

      visual = int(request.POST['visual'])
      visual = gaussian_membership_function(visual, mean_visual,std_visual)
      sensory = int(request.POST['sensory'])
      dysphasia = int(request.POST['dysphasia'])
      dysarthria = int(request.POST['dysarthria'])
      vertigo = int(request.POST['vertigo'])
      tinnitus = int(request.POST['tinnitus'])
      hypoacusis = int(request.POST['hypoacusis'])
      diplopia = int(request.POST['diplopia'])
      defect = int(request.POST['defect'])
      ataxia = int(request.POST['ataxia'])
      conscience = int(request.POST['conscience'])
      paresthesia = int(request.POST['paresthesia'])
      dpf = int(request.POST['dpf'])
      rf = joblib.load('headache_prediction/model_predict/random_forest.joblib')
      predictions = rf.predict(np.array([[age, duration, frequency, location, character, intensity, nausea, vomit, phonophobia, photophobia, visual, sensory, dysphasia, dysarthria, vertigo, tinnitus, hypoacusis, diplopia, defect, ataxia, conscience, paresthesia, dpf ]]))
      label_name = ""
      if predictions[0] == 0:
        label_name = "Đau đầu điển hình không kèm theo chứng tiền triệu"
      elif predictions[0]  == 1:
        label_name = "Đau đầu điển hình kèm theo chứng tiền triệu"
      elif predictions[0]  ==  2:
        label_name = "Đau nửa đầu liệt phân tán"
      elif predictions[0]  ==  3:
        label_name = "Đau nửa đầu khác"
      elif predictions[0]  == 4:
        label_name = "Đau nửa đầu không kèm theo chứng tiền triệu"
      elif predictions[0]  == 5:
        label_name = "Đau nửa đầu liệt phân gia đình"
      elif predictions[0]  == 6:
        label_name = "Chứng tiền triệu kiểu nền sọ"
      method = "POST"
      return render(request,"index.html",{'method':method,'label_name':label_name})