from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import *
# Create your views here.

def home(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        email = User.objects.normalize_email(email)

        
        if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('home')
            
        if  User.objects.filter(email=email).exists():
                messages.error(request, 'email already exists')
                return redirect('home')
            
        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Account created successfully! You can now log in.')
        return redirect('login')
        
            
    return render(request,'index.html')

def loginPage(request):
    user = User.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:   # authentication successful
            login(request, user)
            return redirect('/courses/')
        else:   # authentication failed
            messages.error(request, 'Invalid username or password')
            return redirect('login')  # redirect back to login page
        
    return render(request, 'login.html')


def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def courselist(request):
    courses = Course.objects.all()
    return render(request,'courselist.html',{'courses':courses})

@login_required(login_url='login')
def CourseDetail(request,pk):
    course = Course.objects.get(pk=pk)
    return render(request,'course_detail.html',{'course':course})