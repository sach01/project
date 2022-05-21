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
    text = ("Hello, world. You're at the index.")
    #gfloor = Ground.objects.all().order_by('room')
    #ffloor = First.objects.all().order_by('room')
    #sfloor = Second.objects.all().order_by('room')
    #context = {'gfloor': gfloor, 'ffloor':ffloor, 'sfloor':sfloor}
    #return render(request, 'index.html', context=context)
    return HttpResponse("Hello, world. You're at the polls index.")

@login_required
def duplicate(request):
    #text = ("Hello, world. You're at the index.")
    test = Test.objects.all().values()
    #df = pd.DataFrame(Test.objects.all().values())
    df = pd.DataFrame(test,columns= ['name', 'room'])
    df1 = pd.DataFrame(df.duplicated(subset=('name', 'room')))# working with room too..

    #dup = df[df['dups']].drop_duplicates(subset='room')
    #df.groupby(["name", "room"]).filter(lambda df:df.shape[0] == 1)
    #df['duplicates'] = df.duplicated()
    #df.groupby(["name", "room"]).filter(lambda df:df.shape[0] == 1)
    #df['duplicates'] = df.duplicated()
    #df4 = df.groupby('name')['room'].apply(lambda x: x.unique()).reset_index()#
    
    c1 = df.duplicated()
    c2 = df.groupby(['name','room'])['room'].transform('count').gt(1)
    df['is_duplicate'] = np.where(c2,c1,'Recently Added/Unique')


    #pd.DataFrame(df4,columns= ['is_duplicate'])
    #.set_index('mukey'), on='mukey', how='left'
    #df5 = pd.DataFrame(df4,columns= ['is_duplicate'])
    
    #df['is_duplicate'] = df.duplicated(subset=['name', 'room'])
    #df4.columns[1]
   # df5.reindex(df5.iloc[:,[0,2]]

    #df5 = df.join(df4, how = 'left', lsuffix='left', rsuffix='right')
    #df3 = df.duplicated()
    #df2 = pd.DataFrame(df3)

    # sorting by first name 
    #df.sort_values("name", inplace = True) 
    # dropping ALL duplicte values 
    #df.drop_duplicates()
    #df.drop_duplicates(subset ="name",keep = 'last').reset_index(drop = True) 
    #df.drop_duplicates(subset=['name'])
    #df.drop_duplicates(subset=['name', 'room'], keep=False)
    # displaying data 
    #df.drop_duplicates()
    print(df)
    print(df1)
    #print(df5)
    #print(df2)
    #print(dup)
    #print(dup['room'])
    context = {'test': test, 'df':df.to_html, 'df1':df1.to_html}
    return render(request, 'duplicate.html', context=context)
    #return HttpResponse("Hello, world. You're at the polls index.")

@login_required
def duplicate1(request):
    #text = ("Hello, world. You're at the index.")
    test1 = Test1.objects.all().values()
    #df = pd.DataFrame(test1,columns= ['name', 'room'])
    df = pd.DataFrame(test1,columns= ['name', 'room'])
    #df = pd.DataFrame(test1)
    # sorting by first name 
    ##df.sort_values("room", inplace = True) 
    # dropping ALL duplicte values 
    ##df.drop_duplicates(subset ="room",keep = False, inplace = True) 
    # displaying data 
    c1 = df.duplicated()
    c2 = df.groupby(['name','room'])['room'].transform('count').gt(1)
    df['is_duplicate'] = np.where(c2,c1,'Recently Added/Unique')

    df1 = df.groupby('name')['room'].apply(lambda x: x.unique()).reset_index()
    print(df1)
    print(df)

    context = {'test1': test1, 'df':df.to_html, 'df1':df1.to_html}
    return render(request, 'duplicate1.html', context=context)

@login_required
def duplicate2(request):
    #text = ("Hello, world. You're at the index.")
    test2 = Test2.objects.all().values()
    df = pd.DataFrame(test2, columns = ['name', 'room', 'is_duplicate'])
    #df.columns = ['name', 'room']
    # sorting by first name 
    #df.sort_values("room", inplace = True) 
    # dropping ALL duplicte values 
    #df.drop_duplicates(subset ="room",keep = False, inplace = True) 
    # displaying data 
    
    c1 = df.duplicated()
    #c1 = df[~df.index.duplicated(keep='first')]
    c2 = df.groupby(['name','room'])['room'].transform('count').gt(1)
    df['is_duplicate'] = np.where(c2,c1,'Recently Added/Unique')
    

    #df3 = df[~df.index.duplicated(keep='first')]
    #df3 = pd.DataFrame([df]).transpose()
    #df3.columns = ['name', 'room', 'is_duplicate']
    df3 = pd.DataFrame(df)
    df3[~df3.index.duplicated(keep='first')]
    #df3 = pd.DataFrame(np.array([df]), 
    #columns=['name', 'room'],['is_duplicate'])
    #df3 = df
    print(df)
    print(df3)
    context = {'test2': test2, 'df':df.to_html, 'df3': df3.to_html}
    return render(request, 'duplicate2.html', context=context)

@login_required
def final(request):
    #text = ("Hello, world. You're at the index.")
    final = Final.objects.all().values()
    df = pd.DataFrame(final, columns = ['name', 'room', 'status'])
    #df.columns = ['name', 'room']
    # sorting by first name 
    #df.sort_values("room", inplace = True) 
    # dropping ALL duplicte values 
    #df.drop_duplicates(subset ="room",keep = False, inplace = True) 
    # displaying data 
    
    ##c1 = df.duplicated()
    #c1 = df[~df.index.duplicated(keep='first')]
    ##c2 = df.groupby(['name','room'])['room'].transform('count').gt(1)
    ##df['is_duplicate'] = np.where(c2,c1,'Recently Added/Unique')
    

    #df3 = df[~df.index.duplicated(keep='first')]
    #df3 = pd.DataFrame([df]).transpose()
    #df3.columns = ['name', 'room', 'is_duplicate']
    ##df3 = pd.DataFrame(df)
    ##df3[~df3.index.duplicated(keep='first')]
    #df3 = pd.DataFrame(np.array([df]), 
    #columns=['name', 'room'],['is_duplicate'])
    #df3 = df
    ##print(df)
    ##print(df3)
    context = {'final': final}
    return render(request, 'final.html', context=context)


@login_required
def final1(request):
    #text = ("Hello, world. You're at the index.")
    final1 = Final1.objects.all().values()
    #df = pd.DataFrame(final1, columns = ['name', 'room', 'status'])

    context = {'final1': final1}
    return render(request, 'final1.html', context=context)

@login_required
def final2(request):
    #text = ("Hello, world. You're at the index.")
    final2 = Final2.objects.all().values()
    #df = pd.DataFrame(final1, columns = ['name', 'room', 'status'])

    context = {'final2': final2}
    return render(request, 'final2.html', context=context)

@login_required
def vacant(request):
    #text = ("Hello, world. You're at the index.")
    vacant = Vacant.objects.all().values()
    df = pd.DataFrame(vacant, columns = ['name', 'room'])

    #df.columns = ['name', 'room']
    # sorting by first name 
    df.sort_values("room", inplace = True) 
    # dropping ALL duplicte values 
    df.drop_duplicates(subset ="room",keep = False, inplace = True) 
    # displaying data 

    ##c1 = df.duplicated()
    #c1 = df[~df.index.duplicated(keep='first')]
    ##c2 = df.groupby(['name','room'])['room'].transform('count').gt(1)
    ##df['is_duplicate'] = np.where(c2,c1,'Recently Added/Unique')

    df3 = pd.DataFrame(df)
    df3[~df3.index.duplicated(keep='first')]

    print(df)
    print(df3)
    context = {'vacant': vacant, 'df':df.to_html, 'df3': df3.to_html}
    return render(request, 'vacant.html', context=context)

@login_required
def vacant1(request):
    #text = ("Hello, world. You're at the index.")
    vacant1 = Vacant1.objects.all().values()
    df = pd.DataFrame(vacant1, columns = ['name', 'room'])

    #df.columns = ['name', 'room']
    # sorting by first name 
    df.sort_values("room", inplace = True) 
    # dropping ALL duplicte values 
    df.drop_duplicates(subset ="room",keep = False, inplace = True) 
    # displaying data 

    ##c1 = df.duplicated()
    #c1 = df[~df.index.duplicated(keep='first')]
    ##c2 = df.groupby(['name','room'])['room'].transform('count').gt(1)
    ##df['is_duplicate'] = np.where(c2,c1,'Recently Added/Unique')

    df3 = pd.DataFrame(df)
    df3[~df3.index.duplicated(keep='first')]

    print(df)
    print(df3)
    context = {'vacant1': vacant1, 'df':df.to_html, 'df3': df3.to_html}
    return render(request, 'vacant1.html', context=context)

@login_required
def vacant2(request):
    #text = ("Hello, world. You're at the index.")
    vacant2 = Vacant2.objects.all().values()
    df = pd.DataFrame(vacant2, columns = ['name', 'room'])

    #df.columns = ['name', 'room']
    # sorting by first name 
    df.sort_values("room", inplace = True) 
    # dropping ALL duplicte values 
    df.drop_duplicates(subset ="room",keep = False, inplace = True) 
    # displaying data 

    ##c1 = df.duplicated()
    #c1 = df[~df.index.duplicated(keep='first')]
    ##c2 = df.groupby(['name','room'])['room'].transform('count').gt(1)
    ##df['is_duplicate'] = np.where(c2,c1,'Recently Added/Unique')

    df3 = pd.DataFrame(df)
    df3[~df3.index.duplicated(keep='first')]

    print(df)
    print(df3)
    context = {'vacant2': vacant2, 'df':df.to_html, 'df3': df3.to_html}
    return render(request, 'vacant2.html', context=context)

@login_required
def vacant3(request):
    #text = ("Hello, world. You're at the index.")
    test2 = Test2.objects.all().values()
    df = pd.DataFrame(test2,columns= ('name', 'room'))
    # sorting by first name 
    #df.sort_values("room", inplace = True) 
    # dropping ALL duplicte values 
    #df.drop_duplicates(subset ="room",keep = False, inplace = True) 
    # displaying data 
    #print(df)

    df = pd.DataFrame(test2,columns= ['room', 'room1'])
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
    context = {'test2': test2, 'df':df.to_html}
    return render(request, 'duplicate2.html', context=context)

@login_required
def gpayment(request):
    #text = ("Hello, world. You're at the index.")
    gpayment = Gpayment.objects.all()
    #gpayment = pd.DataFrame(gpayment)

    context = {'gpayment': gpayment}
    return render(request, 'gpayment.html', context=context)
