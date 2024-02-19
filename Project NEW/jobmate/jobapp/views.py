from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.encoding import force_str

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import datetime

from django.contrib.auth import logout
import hashlib
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.cache import never_cache

from .models import Job_Seekers, Job_Providers,User,PostJobs,account_activation_token,ApplyJob,Rating,SavedJob
def home(request):
    return render(request, "home.html")

from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse



class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.is_active}"

generate_token = TokenGenerator()

def register(request):
    if request.method == 'POST':
        # Extract form data
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        dob = request.POST['dob']  # Assuming dob is in 'YYYY-MM-DD' format
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
      

        if User.objects.filter(email=email).exists():
            messages.error(request, 'User with this email already exists. Please use a different email.')
        else:
            # Create a user instance
            user = User.objects.create_user(username=email, password=password, first_name=first_name, last_name=last_name, email=email)

            # Create a JobSeeker instance
            seeker = Job_Seekers(
                user=user, dob=dob, gender=gender, loc=loc, phone=phone,
                qual=qual, oqual=oqual, skills=skills, exp=exp,
                aadhaar=aadhaar, pro_pic=pro_pic, resume=resume
            )
            seeker.save()

            # Generate a token for this user
            token = account_activation_token.make_token(user)

            # Get current site
            current_site = get_current_site(request)

            # Create email body
            mail_subject = 'Activate your account.'
            message = render_to_string('emailactivate.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
            })

            # Send email
            send_mail(mail_subject, message, 'jobmate2023@gmail.com', [email])

            messages.success(request, 'Registration successful. Check your email for verification.')
            return redirect('login')

    return render(request, 'register.html')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if account_activation_token.check_token(user, token):
            user.is_verified = True
            user.save()
            messages.success(request, 'Email confirmed. You can now login.')
            return redirect('login')
        else:
            messages.error(request, 'Activation link is invalid!')
            return redirect('login')
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, 'Activation link is invalid!')
        return redirect('login')


from django.core.mail import send_mail  # Add this import statement

def companyreg(request):
    if request.method == 'POST':
        # Extract form data
        cname = request.POST.get('cname', '')
        email = request.POST.get('email', '')
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

        # Check if a user with this email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'User with this email already exists. Please sign in.')
        else:
            # Create a user instance
            user = User.objects.create_user(username=email, password=password, first_name=cname, role=User.Role.JOBPROVIDER, email=email)

            
            # Create a JobProvider instance
            provider = Job_Providers(
                user=user,
                cname=cname,
                ceoname=ceoname,
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

            # Get current site
            current_site = get_current_site(request)

            # Create email body
            mail_subject = 'Activate your account.'
            message = render_to_string('emailactivate.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            # Send email
            send_mail(mail_subject, message, 'jobmate2023@gmail.com', [email])

            messages.success(request, 'Registration successful. Check your email for verification.')
            return redirect('login')

    return render(request, 'companyreg.html')




#from django.contrib.sessions.models import Session
#Session.objects.all().delete()

@never_cache
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.role == User.Role.ADMIN:
                login(request, user)
                request.session['user_role'] = user.role
                return redirect('admindash')
            elif user.role == User.Role.JOBSEEKER:
                login(request, user)
                request.session['user_id'] = user.id
                request.session['f_name'] = f"{user.first_name} {user.last_name}"
                request.session['user_role'] = 'jobseeker'
                seeker, created = Job_Seekers.objects.get_or_create(user=user)
                pro_pic_url = seeker.pro_pic.url
                request.session['userimg'] = pro_pic_url
                return redirect('userdash')
            elif user.role == User.Role.JOBPROVIDER:
                #if not user.is_verified:
                 #   messages.success(request, 'Please verify your email to continue.')
                  #  request.session.flush()
                   # logout(request)
                    #return render(request, 'login.html')

                if not user.is_active:
                    messages.warning(request, 'Your registration is awaiting approval by the Administrator.')
                    return render(request, 'verification_pending.html')

                login(request, user)
                request.session['user_id'] = user.id
                request.session['user_name'] = user.first_name
                request.session['user_role'] = 'jobprovider'
                
                try:
                    provider = Job_Providers.objects.get(user=user)
                    logo_url = provider.logo.url
                    is_active = user.is_active
                    request.session['userimg'] = logo_url
                    request.session['status'] = is_active

                    if is_active:
                        return redirect('companydash')
                    else:
                        messages.warning(request, 'Your registration is awaiting approval by the Administrator.')
                        return render(request, 'verification_pending.html')

                except Job_Providers.DoesNotExist:
                    messages.warning(request, 'Job Provider details not found.')
                    return render(request, 'verification_pending.html')
            
        else:
            messages.warning(request, 'Invalid email or password. Please try again.')

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
        try:
            provider = Job_Providers.objects.get(user=user)
            return render(request, 'companydash.html')
        except Job_Providers.DoesNotExist:
            
            provider = Job_Providers.objects.create(user=user)
            return render(request, 'companydash.html')
    elif user.role == User.Role.JOBSEEKER:
        try:
            seeker = Job_Seekers.objects.get(user=user)
            return render(request, 'userdash.html')
        except Job_Seekers.DoesNotExist:
            # If Job_Seekers profile doesn't exist, you might want to handle this
            # differently for social logins. For now, let's create a new Job_Seekers
            # profile for the user.
            seeker = Job_Seekers.objects.create(user=user)
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



    return render(request, 'seekerpro.html',{'seeker': seeker})

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

    user_id = request.session.get('user_id')
    seeker = Job_Seekers.objects.get(user_id=user_id)
    return render(request, 'seekerupdate.html',{'seeker': seeker})  

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

# views.py
def search_jobs(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query', '')
        jobs = PostJobs.objects.filter(title__icontains=search_query)
        return render(request, 'searchjobs.html', {'query': search_query, 'jobs': jobs})
    else:
        return render(request, 'searchjobs.html', {})

def search_seeker(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query', '')
        seekers = Job_Seekers.objects.filter(skills__icontains=search_query)
        return render(request, 'searchcandi.html', {'query': search_query, 'seekers': seekers})
    else:
        return render(request, 'searchcandi.html', {})

#def search_loc(request):
 #   if request.method == 'POST':
  #      search_query = request.POST.get('search_query', '')
   #     jobs = PostJobs.objects.filter(location__icontains=search_query)
    #    return render(request, 'searchloc.html', {'query': search_query, 'jobs': jobs})
    #else:
     #   return render(request, 'searchloc.html', {})

from django.db.models import Q


def search_loc(request):
    if request.method == 'POST':
        search_query_job = request.POST.get('search_query_job', '')
        search_query_loc = request.POST.get('search_query_loc', '')

        # Use Q objects to combine multiple queries
        combined_query = Q()

        # Check if title search term is present
        if search_query_job:
            combined_query &= Q(title__icontains=search_query_job)

        # Check if location search term is present
        if search_query_loc:
            combined_query &= Q(location__icontains=search_query_loc)

        # Use the combined Q object in the filter
        jobs = PostJobs.objects.filter(combined_query)

        return render(request, 'searchloc.html', {'query_job': search_query_job, 'query_loc': search_query_loc, 'jobs': jobs})
    else:
        return render(request, 'searchloc.html', {})

def seekerview(request):
    seekers = Job_Seekers.objects.all()
    # Implement any custom logic here
    return render(request, 'companydash.html', {'seekers': seekers})


def post_job(request):
    user_id = request.session.get('user_id')
    
    # Check if the user is logged in
    if not user_id:
        return HttpResponse("User not logged in.")  # You can customize this response

    # Check if the Job_Providers profile exists for the logged-in user
    try:
        job_provider = Job_Providers.objects.get(user_id=user_id)
    except Job_Providers.DoesNotExist:
        return HttpResponse("Job_Providers profile does not exist. Please create your profile first.")

    if request.method == 'POST':
        # Get the form data from the POST request
        title = request.POST.get('title')
        type = request.POST.get('type')
        location = request.POST.get('location')
        description = request.POST.get('description')
        requirements = request.POST.get('requirements')
        experience_required = request.POST.get('experience_required')
        category = request.POST.get('category')
        status = request.POST.get('status')
        min_salary = request.POST.get('min_salary')
        max_salary = request.POST.get('max_salary')
        deadline = request.POST.get('deadline')
        mode = request.POST.get('mode')

        # Create and save a new PostJobs instance with the form data
        post_job = PostJobs(
            title=title,
            type=type,
            location=location,
            description=description,
            requirements=requirements,
            minexp=experience_required,
            pro_id=job_provider,  # Assign the Job_Providers instance
            status=status,
            min_salary=min_salary,
            max_salary=max_salary,
            deadline=deadline,
            mode=mode
        )

        post_job.save()
        # Optionally, you can perform additional actions here, like sending email notifications or performing other logic.
        return redirect('companydash')  # You can customize the response message

    return render(request, 'postjob.html')




def posted_jobs(request):
    jobs = PostJobs.objects.all()
    return render(request, 'viewpostedjobs.html', {'jobs': jobs})



def admin(request):
    candidates=Job_Seekers.objects.count()
    companies=Job_Providers.objects.count()
    
def companylist(request):
    

    companies = Job_Providers.objects.all()
    return render(request, 'companylist.html', {'companies': companies})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from django.contrib.auth import authenticate, login

def changepw_seeker(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # Redirect to login if the user is not authenticated

    b = Job_Seekers.objects.filter(user_id=user_id).first()

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        current_password = request.POST.get('current_password')
        confirm_password = request.POST.get('confirm_password')
       

        if new_password != confirm_password:
            context = {'msg': 'Passwords do not match', 'msg_type': 'error'}
            return render(request, 'changepw_seeker.html', {'b': b, 'msg': context})
        if current_password == new_password:
            context = {'msg': 'Please use a different password than your old password', 'msg_type': 'error'}
            return render(request, 'changepw_seeker.html', {'b': b, 'msg': context})

        user = authenticate(request, email=b.user.email, password=current_password)

        if user is not None:
            user.set_password(new_password)
            user.save()

            # Re-authenticate the user with the new credentials
            user = authenticate(request, email=b.user.email, password=new_password)

            if user is not None:
                login(request, user)
                context = {'msg': 'Password Changed Successfully', 'msg_type': 'success'}
                return render(request, 'login.html', {'b': b, 'msg': context})
            else:
                context = {'msg': 'Failed to re-authenticate after changing the password', 'msg_type': 'error'}
                return render(request, 'changepw_seeker.html', {'b': b, 'msg': context})
        else:
            context = {'msg': 'Your Old Password is Wrong', 'msg_type': 'error'}
            return render(request, 'changepw_seeker.html', {'b': b, 'msg': context})

    return render(request, 'changepw_seeker.html', {'b': b})


from django.contrib.auth import authenticate, login

def changepw_pro(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # Redirect to login if the user is not authenticated

    b = Job_Providers.objects.filter(user_id=user_id).first()

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        current_password = request.POST.get('current_password')
        confirm_password = request.POST.get('confirm_password')
        

        if new_password != confirm_password:
            context = {'msg': 'Passwords do not match', 'msg_type': 'error'}
            return render(request, 'changepw_pro.html', {'b': b, 'msg': context})
        if current_password == new_password:
            context = {'msg': 'Please use a different password than your old password', 'msg_type': 'error'}
            return render(request, 'changepw_pro.html', {'b': b, 'msg': context})
        user = authenticate(request, email=b.user.email, password=current_password)

        if user is not None:
            user.set_password(new_password)
            user.save()

            # Re-authenticate the user with the new credentials
            user = authenticate(request, email=b.user.email, password=new_password)

            if user is not None:
                login(request, user)
                context = {'msg': 'Password Changed Successfully', 'msg_type': 'success'}
                return render(request, 'login.html', {'b': b, 'msg': context})
            else:
                context = {'msg': 'Failed to re-authenticate after changing the password', 'msg_type': 'error'}
                return render(request, 'changepw_pro.html', {'b': b, 'msg': context})
        else:
            context = {'msg': 'Your Old Password is Wrong', 'msg_type': 'error'}
            return render(request, 'changepw_pro.html', {'b': b, 'msg': context})

    return render(request, 'changepw_pro.html', {'b': b})


def delete_job(request, job_id):
    job = get_object_or_404(PostJobs, job_id=job_id, pro_id__user=request.user)
    
    if request.method == 'POST':
        job.delete()
        return redirect('companyjobs')
        
    return render(request, 'deletejob.html', {'job': job})

def viewjobdetails(request, job_id):
    job = get_object_or_404(PostJobs, job_id=job_id)
    return render(request, 'jobdetails.html', {'job': job})

    
def edit_job(request, job_id):
    job = get_object_or_404(PostJobs, job_id=job_id, pro_id__user=request.user)

    if request.method == 'POST':
        # Handle form data directly in the view
        job.title = request.POST.get('title')
        job.type = request.POST.get('type')
        job.location = request.POST.get('location')
        job.description = request.POST.get('description')
        job.requirements = request.POST.get('requirements')
        job.minexp = request.POST.get('minexp')
        job.status = request.POST.get('status')
        job.min_salary = request.POST.get('min_salary')
        job.max_salary = request.POST.get('max_salary')
        job.deadline = request.POST.get('deadline')
        job.mode = request.POST.get('mode')

        job.save()
        return redirect('companyjobs')
        messages.warning(request, 'Updated successfully.')


    return render(request, 'editjob.html', {'job': job})



def delete_job_by_company(request, job_id):
    # Get the job instance or return a 404 response if not found
    job = get_object_or_404(PostJobs, job_id=job_id)

    if request.method == 'POST':
        # Check if the logged-in user is the owner of the job
        job.delete()
        messages.success(request, 'Job deleted successfully.')
        return redirect('companyjobs')
    else:
        # Render a confirmation page or handle the logic accordingly
        return redirect('companydash')



def companyjobs(request):
    # Get the currently logged-in company
    company = Job_Providers.objects.get(user=request.user)

    # Filter jobs based on the logged-in company
    company_jobs = PostJobs.objects.filter(pro_id=company)
    print(company_jobs)
    return render(request, 'companyjobs.html', {'jobs': company_jobs})


def verifymail(request):
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')

        # Check if the user is authenticated
        if request.user.is_authenticated:
            user = request.user

            # Check if the user has otp and the entered OTP matches
            stored_otp = 123456
            stored_otp_created_at = request.session.get('otp_created_at')

            print(f"Stored OTP: {stored_otp}, Entered Code: {verification_code}")

            if stored_otp is not None and str(stored_otp) == verification_code:
                # Check if the OTP has expired (adjust the expiration time as needed)
                # expiration_time = stored_otp_created_at + timezone.timedelta(minutes=5)
                # if timezone.now() <= expiration_time:
                # OTP is valid
                user.is_verified = True
                user.save()
                messages.success(request, 'Email verification successful. You can now log in.')

                # Clear the OTP-related session data after successful verification
                # request.session.pop('otp', None)
                # request.session.pop('otp_created_at', None)

                return render(request, 'login.html')
                # else:
                # messages.error(request, 'The verification code has expired. Please request a new one.')
            else:
                messages.error(request, 'Invalid verification code. Please try again.')
        else:
            messages.error(request, 'User is not authenticated. Please log in.')

    return render(request, 'verifymail.html')





    # Redirect to the appropriate page after updating the status
    return HttpResponse('Status updated successfully')  



def update_status(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_active = not user.is_active
    user.save()
    return redirect('seekerlist')  # Replace 'your_redirect_view_name' with the actual name of your view

def update_provider_status(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_active = not user.is_active
    user.save()
    return redirect('companylist')



def applyjob(request, job_id):
    job = get_object_or_404(PostJobs, pk=job_id)

    if request.method == 'POST':
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check if the user has already applied for the job
            if ApplyJob.objects.filter(user=request.user, job_id=job).exists():
                messages.warning(request, "You have already applied for this job.")
                return redirect('applied_jobs')  # Redirect to the job listing page

            # Get the associated Job_Seekers instance for the authenticated user
            job_seeker = Job_Seekers.objects.get(user=request.user)

            # Check if the application deadline has passed
            current_time = datetime.now().date()  # Convert to datetime.date
            if current_time > job.deadline:
                messages.warning(request, 'Application deadline has passed. You cannot apply for this job.')
                return redirect('viewpostedjobs')

            # Create a new ApplyJob instance
            application = ApplyJob.objects.create(
                user=request.user,
                job_id=job,
                pro_id=job.pro_id,
                seeker_id=job_seeker,
                application_date=current_time,
                status='Pending',
            )

            messages.success(request, "Application submitted successfully!")
            return redirect('applied_jobs')  # Redirect to the job listing page
        else:
            messages.error(request, "Please log in to apply for the job.")
            return redirect('viewpostedjobs')  # Redirect to the job listing page

    return render(request, 'viewpostedjobs.html', {'job': job})


def appliedjobs(request):
    print("haiii")
    jobs = ApplyJob.objects.filter(user=request.user)
    return render(request, 'appliedjobs.html', {'applied_jobs': jobs})

def companyview(request):     
    companies = Job_Providers.objects.all()

    return render(request, 'companyview.html', {'companies': companies})
    
def delete_job(request, job_id):
    job = get_object_or_404(ApplyJob, id=job_id)

    job.delete()
    return redirect('viewpostedjobs')


def view_applicants(request):
    # Get the currently logged-in company
    company = Job_Providers.objects.get(user=request.user)

    # Get jobs posted by the logged-in company
    company_jobs = PostJobs.objects.filter(pro_id=company)

    # Initialize an empty dictionary to hold job titles and corresponding applications
    job_applications = {}

    # Iterate over each job posted by the company
    for job in company_jobs:
        # Get all applications for the current job
        applications = ApplyJob.objects.filter(job_id=job)

        # Add the job title and corresponding applications to the dictionary
        job_applications[job.title] = applications

    # Render the 'view_applicants.html' template with the job_applications context
    return render(request, 'view_applicants.html', {'job_applications': job_applications})

from django.http import JsonResponse
 

def save_job(request, job_id):
  user = request.user
  job = PostJobs.objects.get(job_id=job_id)

  if SavedJob.objects.filter(user=user, job_id=job).exists():
      messages.warning(request, 'Job is already saved.')
  else:
      SavedJob.objects.create(user=user, job_id=job)
      return redirect('view_saved_jobs') 


  return redirect('viewpostedjobs') 

def unsave_job(request, job_id):
  user = request.user
  job = PostJobs.objects.get(job_id=job_id)
  SavedJob.objects.filter(user=user, job_id=job).delete()
  messages.warning(request, 'Job has been unsaved.')
  return redirect('view_saved_jobs') 


def view_saved_jobs(request):
    user = request.user
    saved_jobs = SavedJob.objects.filter(user=user)
    job_list = [job.job_id for job in saved_jobs]
    return render(request, 'viewsavedjobs.html', {'jobs': job_list})


def add_review1(request):
    # Check if the user has already submitted a review
    if request.method == 'POST':
       title = request.POST['title']
       stars = request.POST['stars']
       comment = request.POST['comment']
       # Get the user instance (assuming the user is logged in)
       user = request.user
       if Rating.objects.filter(user=user).exists():
            messages.warning(request, "You have already submitted feedback.")
       else:
       # Create a new Rating instance
            rating = Rating(user=user, title=title, stars=stars, comment=comment)
       # Save the new Rating instance to the database
            rating.save()
            return redirect('userdash')

            messages.success(request, "Thank you for your review! Your feedback has been submitted.")

       
    else:
       return render(request, 'seekerrating.html')

def add_review2(request):
    if request.method == 'POST':
       title = request.POST['title']
       stars = request.POST['stars']
       comment = request.POST['comment']
       # Get the user instance (assuming the user is logged in)
       user = request.user
       if Rating.objects.filter(user=user).exists():
            messages.warning(request, "You have already submitted feedback.")
       else:
       # Create a new Rating instance
            rating = Rating(user=user, title=title, stars=stars, comment=comment)
       # Save the new Rating instance to the database
            rating.save()
            return redirect('companydash')

            messages.success(request, "Thank you for your review! Your feedback has been submitted.")

       
    else:
       return render(request, 'prorating.html')

def update_user_avg_rating(user):
    # Update the average star rating for the user based on all reviews
    avg_rating = Rating.objects.filter(user=user).aggregate(Avg('stars'))['stars__avg']
    user.avg_rating = avg_rating
    user.save()

def view_all_ratings(request):
    ratings = Rating.objects.all()
    return render(request, 'all_ratings.html', {'ratings': ratings})