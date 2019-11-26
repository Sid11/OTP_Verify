
# https://www.fast2sms.com/dev/bulk?authorization=RU7gXYMpeLvWidrtjK2G3Q8JZyoTzkODE64xbmhBNuwSClqIaFTFqQAdieZmpauwDbRLl5J12s9yhVH7&sender_id=FSTSMS&language=english&route=p&numbers=9867033324&message=Hey%20buddy%20otp:2019&variables=%7BAA%7D%7C%7BCC%7D&variables_values=12345%7Casdaswdx
from django.shortcuts import render, redirect
import requests
import json
import random
from .models import Otp, Verification

def index(request):
	message = ''
	try:
		message = request.session['error_message']
		request.session['error_message'] = ''
	except:
		pass
	return render(request, 'index.html', {'error_message':message})

def otp_send(request):
	if request.method=="POST":
		API_KEY='RU7gXYMpeLvWidrtjK2G3Q8JZyoTzkODE64xbmhBNuwSClqIaFTFqQAdieZmpauwDbRLl5J12s9yhVH7'
		number = request.POST.get('number')
		request.session['number'] = number
		otp_number = str("{:06d}".format(random.randint(100, 999999)))
		message="Hey%20buddy,%20your%20OTP%20is%20:"+str(otp_number)+"%20from%20finin."
		url = "https://www.fast2sms.com/dev/bulk?authorization="+API_KEY+"&sender_id=FSTSMS&language=english&route=p&numbers="+number+"&message="+message
		# print(url)
		response = requests.request("GET", url)
		
		#Success Response:
		#{'return': True, 'request_id': 'g8e7coavdjl4ui2', 'message': ['Message sent successfully to NonDND numbers']}
		#Failure Response
		#{"return":false,"status_code":411,"message":"Invalid Numbers"}
		result = response.content.decode("utf-8")
		result = json.loads(result)
		# print(result)

		if result['return']:
			#OTP sent successfully
			
			#Update if already exists else create
			#Storage Efficient
			entry = Otp.objects.filter(number=number)
			if entry.count()>0:
				ind = entry[0]
				ind.otp = otp_number
				ind.save()
			else:
				entry = Otp.objects.create(number=number,otp=otp_number)		
			return redirect('otp_verify')
		else:
			#Sending OTP failed
			request.session['error_message'] = result["message"]
			return redirect('index')

		return redirect('index')

def otp_verify(request):
	if request.method=="GET":
		number = request.session['number']
		message = ''
		try:
			message = request.session['invalid_otp']
			request.session['invalid_otp'] = ''
		except:
			pass
		return render(request, 'otp_verify.html', {'number': number, 'error_message':message})
	elif request.method=="POST":
		otp = request.POST.get('otp')
		number = request.session['number']
		if not len(otp)==6:
			request.session['invalid_otp'] = 'Invalid OTP'
			return redirect('otp_verify')

		verify = False
		try:
			verify = Otp.objects.get(number=number, otp=otp)
		except:
			pass
		
		if verify:
			request.session['verified_number'] = number
			return redirect('verify_success') 
		else:
			request.session['invalid_otp'] = 'Invalid OTP'
			return redirect('otp_verify')

def verify_success(request):
	return render(request, 'verify_success.html', {'number':request.session['verified_number']})
	