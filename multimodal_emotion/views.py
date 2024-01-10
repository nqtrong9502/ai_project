from django.shortcuts import render
from django.views.generic import View
class MyViewMultimodalEmotion(View):
  def get(self, request, *args, **kwargs):
    # pass
    return render(request, "index_multimodal_emotion.html")
  def post(self, request, *args, **kwargs):
    method = request.method
    print(request.POST["name"])
    print(request.POST)

    return render(request, "index_multimodal_emotion.html",{'method':method})

    pass
# Create your views here.
