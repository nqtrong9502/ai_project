from django.shortcuts import render
import joblib
import numpy as np
# Create your views here.
from django import forms
from underthesea import text_normalize,word_tokenize
from django.http import HttpResponse
from django.views.generic import View
import torch.nn.functional as F
from torch import nn, Tensor
import torch
from torchtext import data


class LSTMNet(nn.Module):
    def __init__(self,vocab_size,embedding_dim,hidden_dim,output_dim,n_layers):
        super(LSTMNet,self).__init__()
        self.embedding = nn.Embedding(vocab_size,embedding_dim)
        head = 4
        layer = 6
        self.ga0 = nn.MultiheadAttention(embedding_dim, head, dropout = 0.03)
        self.lstm = nn.LSTM(embedding_dim,
                            hidden_dim,
                            num_layers = n_layers,
                            batch_first = False,
                            bidirectional = True,
                            dropout= 0.03
                           )
        self.fc0 = nn.Linear(hidden_dim*2 ,hidden_dim)
        self.batch_norm_1 =  nn.BatchNorm1d(hidden_dim)
        self.fc1 = nn.Linear(hidden_dim ,output_dim)
    def forward(self,text,text_lengths):
        text = torch.transpose(text,1,0)
        embedded0 = self.embedding(text)

        # Attention
        embedded0, w = self.ga0(embedded0, embedded0, embedded0)
        # LSTM
        packed_output,(hidden_state, cell_state) = self.lstm(embedded0)
        h = torch.cat((hidden_state[-1,:,:], hidden_state[-2,:,:]), dim = 1)
        h = self.fc0(h)
        h = F.selu(h)
        h = self.fc1(h)
        h = F.sigmoid(h)
        return h
texg = torch.load('detecttext/vocab_obj.pth')
SIZE_OF_VOCAB = len(texg.vocab)
EMBEDDING_DIM = 64
NUM_HIDDEN_NODES = 64
NUM_OUTPUT_NODES = 1
NUM_LAYERS = 2
model = LSTMNet(SIZE_OF_VOCAB,
                EMBEDDING_DIM,
                NUM_HIDDEN_NODES,
                NUM_OUTPUT_NODES,
                NUM_LAYERS,
               )
model.load_state_dict(torch.load("detecttext/sub/model_text_attention_lstm_classification.pth", map_location=torch.device('cpu')))

# optimizer = torch.optim.Adam(model.parameters(),lr=0.01)
criterion = nn.BCELoss()

class MyViewDetecttext(View):
  def get(self, request, *args, **kwargs):
    return render(request,"detecttext.html")
  def post(self, request, *args, **kwargs):
    if request.method == "POST":
      text = request.POST['text']
      text = text_normalize(text)
      text = word_tokenize(text)
      transform_text = torch.Tensor([ texg.vocab.stoi[i] for i in text]).long().unsqueeze(0)
      re = model(transform_text,1)
      if re[0][0] < 0.5:
        text = "Tích cực"
      else:
        text = "Tiêu cực"
      return render(request,"detecttext.html",{'method':request.method,'label_name':re.item(),'text':text})