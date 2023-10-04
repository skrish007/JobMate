
from django.db import models
from PIL import Image

from datetime import date
from django.urls import reverse
#Admin

#Job Seekers Database
class Job_Seekers(models.Model):
    
    id = models.AutoField(primary_key=True)
    first_name = models.CharField("First Name", max_length=50)
    last_name = models.CharField("Last Name", max_length=50)
    dob = models.DateField("Date of Birth", default=date.today)
    loc = models.CharField("Location", max_length=50)
    phone = models.CharField("Phone No", max_length=10)
    qual = models.CharField("Qualification", max_length=25)
    oqual = models.CharField("Other Qualification", max_length=25)
    exp = models.CharField("Work Experience", max_length=25)
    skills = models.CharField("Skills", max_length=150)
    resume = models.FileField("Upload Resume", upload_to='candidate/resume/', max_length=254, default=0)
    aadhaar = models.CharField("Aadhaar No", max_length=25)
    pro_pic = models.FileField("Upload Photos", upload_to='candidate/images/', max_length=254, default=0)
    role = models.CharField(max_length=100, default='candidate')
    email = models.EmailField(unique=True)

    password=models.CharField(max_length=20)
    
   
    
#JobProviders DataBase
class Job_Providers(models.Model):
    #Company Information
    email = models.EmailField(max_length=100, unique=True)
    cname = models.CharField('Name', max_length=50)
    ceoname = models.CharField('CEO Name', max_length=50)
    caddress = models.CharField('Company Address', max_length=150)
    ctype = models.CharField('Company Type', max_length=25)
    otherctype = models.CharField('Company Type', max_length=25)
    cdescription = models.CharField('Company Description', max_length=500)
    cphone = models.CharField('Company Phone Number',max_length=20)
    website = models.CharField('Company Website', max_length=100)
    empno = models.IntegerField('No Of Employees')
    fyear = models.IntegerField('Founded Year')
    logo = models.ImageField('Company Logo in jpg/png Format', upload_to='company/')
    clicense = models.CharField('License number', max_length=100)
    licensefile = models.FileField('Company Licence in pdf Format', upload_to='license/')
    status = models.CharField('Current Status', max_length=20, default='Not Verified')
    is_verified = models.BooleanField('Verification Status', default=False)
    role = models.CharField(max_length=100, default='provider')
    password = models.CharField(max_length=20)
    