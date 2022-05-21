from django.shortcuts import render, redirect
from django.http import HttpResponse
#from auto.models import Final, Final1, Final2, Vacant, Vacant1, Vacant2, Groom, Froom, Sroom, Ground, First, Second, Gpayment, Fpayment, Spayment, Test, Test1, Test2
#from django.utils.html import format_html
#from .forms import GroundForm
from django.forms import ModelForm
from django.contrib import messages
from django_pandas.io import read_frame
import pandas as pd
import numpy as np
from django_pandas.io import read_frame
#from django.db import models
# Create your views here.
from django.conf import settings
#from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import auth 
from django.db.models import Avg, Count, Min, Sum
from django.db.models.functions import ExtractMonth

def signup(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.get(username = request.POST['username'])
                return render (request,'signup.html', {'error':'Username is already taken!'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                auth.login(request,user)
                return redirect('index')
        else:
            return render (request,'login.html', {'error':'Password does not match!'})
    else:
        return render(request,'signup.html')


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password = request.POST['password'])
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            return render (request,'login.html', {'error':'Username or password is incorrect!'})
    else:
        return render(request,'login.html')

def logout(request):
    if request.method == 'POST':
        if request.user.is_authenticated() and not request.user.is_active:
                        logout(request)
        #auth.logout(request)
    return redirect('/login')

#@login_required(login_url='/login/')
@login_required
def index(request):
    #text = ("Hello, world. You're at the index.")
    #gfloor = Ground.objects.all().order_by('room')
    #ffloor = First.objects.all().order_by('room')
    #sfloor = Second.objects.all().order_by('room')
    #context = {'gfloor': gfloor, 'ffloor':ffloor, 'sfloor':sfloor}
    return render(request, 'index.html', context=context)
    #return HttpResponse("Hello, world. You're at the polls index.")
