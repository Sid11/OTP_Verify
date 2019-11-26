from django.db import models

# Create your models here.


class Otp(models.Model):
	number = models.CharField(max_length=10, blank=False)
	otp = models.CharField(max_length=6, blank=False)

class Verification(models.Model):
	number = models.CharField(max_length=10, blank=False) 
	STATUS_CHOICES = (("Verified", "Verified"), ("Not Verified", "Not Verified"))
	status = models.CharField(blank=False, max_length=20, choices=STATUS_CHOICES)
		