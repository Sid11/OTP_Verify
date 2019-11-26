from django.urls import path
from . import views

# app_name = 'website'

urlpatterns = [

	path('', views.index, name='index'),
	path('otp_send/', views.otp_send, name='otp_send'),
	path('otp_verify/', views.otp_verify, name='otp_verify'),
	path('verify_success/', views.verify_success, name='verify_success'),

]
