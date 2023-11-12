
from django.db import models
from PIL import Image

from datetime import date
from django.urls import reverse
#Admin
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    email=models.EmailField(max_length=100,unique=True)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name', 'last_name','username']
    class Role(models.TextChoices):
        JOBPROVIDER = 'jobprovider', 'Job Provider'
        JOBSEEKER = 'jobseeker', 'Job Seeker'
        ADMIN = 'admin', 'Admin'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.JOBSEEKER,
    )
class Client(User):
    class meta:
        proxy:True

#Job Seekers Database
GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('not-specified', 'Prefer not to say'),
]
class Job_Seekers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    seeker_id = models.AutoField(primary_key=True)
    dob = models.DateField("Date of Birth", default=date.today)
    loc = models.CharField("Location", max_length=50)
    phone = models.CharField("Phone No", max_length=10)
    qual = models.CharField("Qualification", max_length=25)
    oqual = models.CharField("Other Qualification", max_length=25)
    exp = models.CharField("Work Experience", max_length=25)
    skills = models.CharField("Skills", max_length=150)
    resume = models.FileField("Upload Resume", upload_to='seeker/resume/', max_length=254, default=0)
    aadhaar = models.CharField("Aadhaar No", max_length=25)
    pro_pic = models.FileField("Upload Photos", upload_to='seeker/images/', max_length=254, default=0)
    gender = models.CharField("Gender", max_length=20, choices=GENDER_CHOICES, default='not-specified')
   
    
#JobProviders DataBase
class Job_Providers(models.Model):
    #Company Information
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pro_id= models.IntegerField(primary_key=True)
    cname = models.CharField('Name', max_length=50)
    ceoname = models.CharField('CEO Name', max_length=50)
    caddress = models.CharField('Company Address', max_length=150)
    ctype = models.CharField('Company Type', max_length=25)
    otherctype = models.CharField('Other Company Type', max_length=25,blank=True, null=True)
    cdescription = models.CharField('Company Description', max_length=500)
    cphone = models.CharField('Company Phone Number',max_length=10)
    website = models.CharField('Company Website', max_length=100)
    empno = models.IntegerField('No Of Employees')
    fyear = models.DateField('Founded Date')
    logo = models.ImageField('Company Logo in jpg/png Format', upload_to='provider/logo')
    clicense = models.CharField('License number', max_length=100)
    licensefile = models.FileField('Company Licence in pdf Format', upload_to='provider/license/')
    status = models.CharField('Current Status', max_length=20, default='Not Verified')
    

class PostJobs(models.Model):
    ONLINE = 'Online'
    OFFLINE = 'Offline'
    BOTH = 'Both'

    MODE_CHOICES = [
        (ONLINE, 'Online'),
        (OFFLINE, 'Offline'),
        (BOTH, 'Both'),
    ]

    FULL_TIME = 'Full-Time'
    PART_TIME = 'Part-Time'
    CONTRACT = 'Contract'

    TYPE_CHOICES = [
        (FULL_TIME, 'Full-Time'),
        (PART_TIME, 'Part-Time'),
        (CONTRACT, 'Contract'),
    ]
    job_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=FULL_TIME)
    location = models.CharField(max_length=255)
    description = models.TextField()  # Job Description
    requirements = models.TextField()  # Job Requirements
    minexp = models.CharField(max_length=10, default='Fresher')
    pro_id = models.IntegerField(default=1)
    status = models.CharField(max_length=20)  # Job Status, e.g., Open, Closed
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set to the current time
    salary = models.TextField(default='NOT DISCLOSED')
    deadline = models.DateField(null=True)  # Application Deadline
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default=ONLINE)  # Online, Offline, Both

    def __str__(self):
        return self.title