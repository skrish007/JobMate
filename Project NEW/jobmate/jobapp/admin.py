from django.contrib import admin
from .models import *
from django.urls import reverse
from .models import Job_Providers



admin.site.register(Job_Seekers)

admin.site.register(Job_Providers)