from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import PostingForm
from .models import Posting
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'mainpage/home.html')

# Create your views here.
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'mainpage/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('myposts')
            except IntegrityError:
                return render(request, 'mainpage/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'mainpage/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def loginuser(request):
        if request.method == 'GET':
            return render(request, 'mainpage/loginuser.html', {'form':AuthenticationForm()})
        else:
            user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
            if user is None:
                return render(request, 'mainpage/loginuser.html', {'form':AuthenticationForm(), 'error':"Username and password did not match."})
            else:
                login(request, user)
                return redirect('myposts')

@login_required
def createposting(request):
    if request.method == 'GET':
        return render(request, 'mainpage/createposting.html', {'form':PostingForm()})
    else:
        try:
            form = PostingForm(request.POST)
            newposting = form.save(commit=False)
            newposting.UserID = request.user
            newposting.save()
            return redirect('myposts')
        except ValueError:
            return render(request, 'mainpage/createposting.html', {'form':PostingForm(), 'error':'Bad Data'})

@login_required
def myposts(request):
    postings = Posting.objects.raw('SELECT * FROM mainpage_Posting WHERE UserID_id = %s', [request.user.pk])
    return render(request, 'mainpage/myposts.html', {'postings':postings})

def viewposting(request, posting_pk):
    posting = get_object_or_404(Posting, pk=posting_pk, UserID=request.user)
    if request.method == 'GET':
        form = PostingForm(instance=posting)
        return render(request, 'mainpage/viewposting.html', {'posting':posting, 'form':form})
    else:
        try:
            form = PostingForm(request.POST, instance=posting)
            form.save()
            return redirect('myposts')
        except ValueError:
            return render(request, 'mainpage/myposts.html', {'posting':posting, 'form':form ,'error':"Bad Data"})

@login_required
def deleteposting(request, posting_pk):
    posting = get_object_or_404(Posting, pk=posting_pk, UserID=request.user)
    if request.method == 'POST':
        posting.delete()
        return redirect('myposts')
