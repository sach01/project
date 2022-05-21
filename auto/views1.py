from django.shortcuts import render, redirect
from django.http import HttpResponse
from auto.models import Groom, Froom, Sroom, Ground, First, Second, Gpayment, Fpayment, Spayment
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
    #text = ("Hello, world. You're at the polls index.")
    gfloor = Ground.objects.all().order_by('room')
    ffloor = First.objects.all().order_by('room')
    sfloor = Second.objects.all().order_by('room')
    context = {'gfloor': gfloor, 'ffloor':ffloor, 'sfloor':sfloor}
    return render(request, 'index.html', context=context)
    #return HttpResponse("Hello, world. You're at the polls index.")


def second(request):
    second = Second.objects.all().values()
    df = pd.DataFrame(second,columns= ['owner', 'room'])
    print (df.columns)
    df['room'] = df['room'].str[1:]
    
    test_set = df['room']
    low, high = 1, 155
    res = []
    for i in range(low, high):
    # getting elements not in set
        if i not in test_set:
            res.append(i)
    print (test_set)
    print ('C'+str(res))
    #df1 = pd.DataFrame(res)
    df1 = pd.DataFrame(res,columns= ['room'])
    print (df1)

    df2 = pd.DataFrame(df1)
    res1 = []
    for i in df2['room']:
        x = str(i)
        c = 'C'
        res1.append(i)

    df2["room"] = 'B' + df2["room"].astype(str)
    print(df2)
    print (df2)
    #print (df3)
    df = df.reset_index()
    df2 = df2.reset_index()

    vc = df.combine_first(df2)
    print (df2.head())
    context={
        'df':df.to_html(),
        'df1':df1.to_html(),
        #'df4':df4.to_html(),
        'vc':vc.to_html(),
        'second': second,
    }
    return render(request,'second.html',{'vc':vc.to_html(), 'second': second, 'df1':df1.to_html()})


def first(request):
    first = First.objects.all().order_by('room')
    a = First.objects.filter(status= 'vacant')
    context = {'first': first, 'a':a}
    return render(request, 'first.html', context=context)

'''
def ground(request, pk):
	form=GroundForm
	if request.method=='POST':
		form=GroundForm(request.POST,request or None)
		if form.is_valid():
			form.save()
		messages.success(request, 'form has been submitted')
		return redirect('/')
	else:
		context={
        'form':form,
    }
	return render(request,'stall.html',context)
'''

def gfloor(request):
    #text = ("Hello, world. You're at the polls index.")
    all_stall = Stall.objects.all()
    #.order_by('room')

    context = {'all_stall': all_stall}
    return render(request, 'gfloor.html', context=context)
    #return HttpResponse("Hello, world. You're at the polls index.")

def payment(request):
    
    m = Stall.objects.annotate(month=ExtractMonth('check_in')) .values('month').annotate(count=Count('month')).values('month', 'count') 

    context = {'m': m}
    return render(request, 'payment.html', context=context)