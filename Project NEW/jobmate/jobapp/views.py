from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
import hashlib
from django.views.decorators.cache import never_cache

from .models import Job_Seekers, Job_Providers,User

def home(request):
    return render(request, "home.html")

def register(request):
    if request.method == 'POST':
        # Extract form data
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        dob = request.POST['dob']
        gender = request.POST['gender']
        loc = request.POST['loc']
        phone = request.POST['phone']
        qual = request.POST['qual']
        oqual = request.POST['oqual']
        skills = request.POST['skills']
        exp = request.POST['exp']
        aadhaar = request.POST['aadhaar']
        pro_pic = request.FILES.get('pro_pic')
        resume = request.FILES.get('resume')

        # Check if a user with this email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'User with this email already exists. Please sign in.')
        else:
            user = User.objects.create_user(username=email, password=password,first_name=first_name,last_name=last_name,email=email,)
            login(request, user)

        # Create a JobSeeker instance
            seeker = Job_Seekers(user=user,dob=dob,
                gender=gender,
                loc=loc,
                phone=phone,
                qual=qual,
                oqual=oqual,
                skills=skills,
                exp=exp,
                aadhaar=aadhaar,
                pro_pic=pro_pic,
                resume=resume )
            seeker.save()

            # Create and save a new JobSeeker object
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')

    return render(request, 'register.html')

def companyreg(request):
    if request.method == 'POST':
        # Extract form data
        cname = request.POST.get('cname', '')
        cname = request.POST.get('email', '')
        password = request.POST.get('password', '')
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

        if User.objects.filter(email=email).exists():
            messages.error(request, 'User with this email already exists. Please sign in.')
        else:
            user = User.objects.create_user(username=email, password=password,first_name=cname,last_name=ceoname,email=email,role=User.Role.JOBPROVIDER)
            login(request, user)
            provider = Job_Providers(
                user=user,
                
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
                logo=logo,
                
            )
            provider.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')

    return render(request, 'companyreg.html')

@never_cache
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        
        if user is not None:
            login(request, user)
            request.session['user_role'] = user.role  # Store the user's role in the session
            if user.role == User.Role.ADMIN:
                return redirect('admindash')
            elif user.role == User.Role.JOBSEEKER:
                request.session['user_id'] = user.id
                request.session['f_name'] = f"{user.first_name} {user.last_name}"
                request.session['user_role'] = 'jobseeker'
                return  render(request, 'userdash.html')  # Replace with your jobseeker page URL name
            elif user.role == User.Role.JOBPROVIDER:
    # Set session data for the provider
                request.session['user_id'] = user.id
                request.session['user_name'] = user.first_name
                request.session['user_role'] = 'jobprovider'

    # Get the 'Job_Providers' instance for the current user
                try:
                    provider = Job_Providers.objects.get(user=user)
                    z = provider.status
                    request.session['status'] = z
                except Job_Providers.DoesNotExist:
                    z = 'Not Verified'  # Set a default value if the provider instance doesn't exist

            if z == 'Verified':
                return redirect('companydash')
                
            else:
                
                return render(request, 'verification_pending.html')
        

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('/')

def success_view(request):
    user = request.user
    if user.role == User.Role.ADMIN:
        return render(request, 'admindash.html')
    elif user.role == User.Role.JOBPROVIDER:
        return render(request, 'companydash.html')
    elif user.role == User.Role.JOBSEEKER:
        return render(request, 'userdash.html')
    else:
        messages.error(request, 'Invalid user role.')
        return redirect('login')


from django.contrib.auth.decorators import login_required

@login_required
def seekerpro(request):
    # Get the user's profile information based on the currently logged-in user
    user = request.user  # Assuming the user is logged in
    try:
        seeker = Job_Seekers.objects.get(user=user)
    except Job_Seekers.DoesNotExist:
        profile = None

    context = {
        'seeker': seeker,
    }

    return render(request, 'seekerpro.html', context)

@login_required
def seeker_profile_update(request):
    if request.method == 'POST':
        # Update the user's information
        user = request.user
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()

        # Update or create the JobSeeker profile
        seeker, created = Job_Seekers.objects.get_or_create(user=user)
        seeker.dob = request.POST['dob']
        seeker.gender = request.POST['gender']
        seeker.loc = request.POST['loc']
        seeker.phone = request.POST['phone']
        seeker.qual = request.POST['qual']
        seeker.oqual = request.POST['oqual']
        seeker.skills = request.POST['skills']
        seeker.exp = request.POST['exp']
        seeker.aadhaar = request.POST['aadhaar']
        
        pro_pic = request.FILES.get('pro_pic')
        if pro_pic:
            seeker.pro_pic = pro_pic
        
        resume = request.FILES.get('resume')
        if resume:
            seeker.resume = resume

        seeker.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('userdash')  # Redirect to the user's dashboard on success

    return render(request, 'seekerpro.html')  

@login_required
def providerpro(request):
    # Get the user's profile information based on the currently logged-in user
    user = request.user  # Assuming the user is logged in
    try:
        provider = Job_Providers.objects.get(user=user)
    except Job_Providers.DoesNotExist:
        profile = None

    context = {
        'provider': provider,
    }

    return render(request, 'providerpro.html', context)
@login_required
def provider_profile_update(request):
    # Get the job provider's profile based on the currently logged-in user
    provider = Job_Providers.objects.get(user=request.user)

    if request.method == 'POST':
        # Update the job provider's profile attributes
        provider.cname = request.POST.get('cname')
        provider.ceoname = request.POST.get('ceoname')
        provider.caddress = request.POST.get('caddress')
        provider.ctype = request.POST.get('ctype')
        provider.otherctype = request.POST.get('otherctype')
        provider.cdescription = request.POST.get('cdescription')
        provider.cphone = request.POST.get('cphone')
        provider.website = request.POST.get('website')
        provider.empno = request.POST.get('empno')
        provider.fyear = request.POST.get('fyear')

        # You can handle file uploads (e.g., logo and license file) here
        logo = request.FILES.get('logo')
        if logo:
            provider.logo = logo
        
        licensefile = request.FILES.get('licensefile')
        if licensefile:
            provider.licensefile = licensefile
        # Save the updated profile
        provider.save()

        return redirect('companydash')  # Redirect to the user's profile page (modify the URL as needed)

    return render(request, 'provider_profile_update.html', {'provider': provider})

def verification_pending(request):
    # Your view logic here
    return render(request, 'verification_pending.html')

@never_cache



def seekerlist(request):
    seekers = Job_Seekers.objects.all()
    # Implement any custom logic here
    return render(request, 'seekerlist.html', {'seekers': seekers})



from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import PostJob  # Import your PostJob model

def PostJob(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        title = request.POST.get('title')
        type = request.POST.get('type')
        location = request.POST.get('location')
        description = request.POST.get('description')
        requirements = request.POST.get('requirements')
        experience_required = request.POST.get('experience_required')
        category = request.POST.get('category')
        status = request.POST.get('status')
        mode = request.POST.get('mode')
        salary = request.POST.get('salary')
        deadline = request.POST.get('deadline')
        email_id = request.POST.get('email_id')  # Assuming this is the email associated with the company

        # Create a new job posting instance
        job = PostJob(
            title=title,
            type=type,
            location=location,
            description=description,
            requirements=requirements,
            minexp=minexp,
            status=status,
            mode=mode,
            salary=salary,
            deadline=deadline,
             # Assign the email to the foreign key field
        )
        job.save()
        messages.success(request, 'Job Posted successfully.')
        
        # You can perform additional actions here, like sending email notifications or redirecting to a success page.
        return redirect('alljob', job_id=job.id)  # Redirect to a job detail page, change 'job_detail' to your URL name

    return render(request, 'postjob.html')  # Render the job posting form template

def display(request):
    return render(request,'')


def admin(request):
    candidates=Job_Seekers.objects.count()
    companies=Job_Providers.objects.count()
    
def companylist(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('status'):
                company_id = key.split('_')[-1]
                if value in ('Not Verified', 'Verified'):
                    company = Job_Providers.objects.get(pro_id=company_id)
                    company.status = value
                    company.save()
        return redirect('companylist')

    companies = Job_Providers.objects.all()
    return render(request, 'companylist.html', {'companies': companies})