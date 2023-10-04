import os
from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Q,Count
from django.contrib.auth.hashers import make_password
from .models import *
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from datetime import date
from django.contrib.auth import logout
from django.views.decorators.cache import never_cache
from PIL import Image
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Job_Providers, Job_Seekers

# Create your views here.
def home(request):
    return render(request,"home.html")



def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        dob = request.POST['dob']
        loc = request.POST['loc']
        phone = request.POST['phone']
        qual = request.POST['qual']
        oqual = request.POST['oqual']
        skills = request.POST['skills']
        exp = request.POST['exp']
        aadhaar = request.POST['aadhaar']

        if Job_Seekers.objects.filter(email=email).exists():
            messages.error(request, 'User with this email already exists. Please sign in.')
            return redirect('login')

            hashed_password = make_password(password)

        seeker = Job_Seekers(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            dob=dob,
            loc=loc,
            phone=phone,
            qual=qual,
            oqual=oqual,
            skills=skills,
            exp=exp,
            aadhaar=aadhaar
        )
        seeker.save()
        

            # Redirect to a success page
        return redirect('login')

    return render(request, 'register.html')

def companyreg(request):
    if request.method == 'POST':
        cname = request.POST['cname']
        email = request.POST['email']
        password = request.POST['password']
        ceoname = request.POST.get('ceoname')
        caddress = request.POST.get('caddress')
        ctype = request.POST.get('ctype')
        otherctype = request.POST.get('otherctype')
        cdescription = request.POST.get('cdescription')
        cphone = request.POST.get('cphone')
        website = request.POST.get('website')
        empno = request.POST.get('empno')
        fyear = request.POST.get('fyear')
        clicense = request.POST.get('clicense')
        licensefile = request.FILES.get('licensefile')
        logo = request.FILES.get('logo')
        
        
        # Check if email already exists
        if Job_Providers.objects.filter(email=email).exists():
            msg = 'User Already Exists'
            return render(request, 'login.html',{'msg':msg})

        hashed_password = make_password(password)

        # Create Job_Providers object and save to database
        provider = Job_Providers(
        cname=cname,
        ceoname=ceoname,
        email=email,
        password=password,
        caddress=caddress,
        ctype=ctype,
        otherctype=otherctype,
        cdescription=cdescription,
        cphone=cphone,
        website=website,
        empno=empno,
        fyear=fyear,
        clicense=clicense,
        licensefile=licensefile,
        logo=logo
        )
        provider.save()
        
        messages.success(request, 'Registration successful. You can now log in.')
        # Redirect to login page
        return redirect('login')

    return render(request, 'companyreg.html')




@never_cache
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the user is a job provider
        job_provider = Job_Providers.objects.filter(email=email, password=password).first()

        # Check if the user is a job seeker
        job_seeker = Job_Seekers.objects.filter(email=email, password=password).first()

        # Determine the role and redirect accordingly
        if job_provider:
            # Redirect job providers to their dashboard
            
            request.session['user_id'] = job_provider.id
            request.session['user_name'] = job_provider.cname
            request.session['user_role'] = 'provider'
            print(request.session)  
            return redirect('companydash')
        elif job_seeker:
            # Redirect job seekers to their dashboard
            
            request.session['user_id'] = job_seeker.id
            request.session['user_name'] = f"{job_seeker.first_name} {job_seeker.last_name}"
            request.session['user_role'] = 'seeker'
            print(request.session)  # 'seeker_dashboard'
            return redirect('userdash')
        else:
            context = {'msg': 'Invalid Credentials'}
            return render(request, 'login.html', context)

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    request.session.flush()
    print('Logout Succesfully!')
    
    return redirect('/')

@never_cache
def success_view(request):
    # Check the user's role and render the appropriate dashboard
    user_role = request.session.get('user_role')

    if user_role == 'provider':
        return render(request, 'companydash.html')
    elif user_role == 'seeker':
        return render(request, 'userdash.html')
    else:
        messages.error(request, 'Invalid user role.')
        return redirect('login')

