from django.contrib import admin
from .models import Otp, Verification
# Register your models here.
admin.site.register([Otp, Verification])