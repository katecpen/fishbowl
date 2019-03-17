from django.shortcuts import render 
import pyrebase 


config = {
	'apiKey': "AIzaSyAhaOe24nDVf_6PRgjfffu1PwQss2QI3I4",
	'authDomain': "fishbowl-c47d5.firebaseapp.com",
	'databaseURL': "https://fishbowl-c47d5.firebaseio.com",
	'projectId': "fishbowl-c47d5",
	'storageBucket': "fishbowl-c47d5.appspot.com",
	'messagingSenderId': "230121294113"
}



	
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
	
	
def singIn(request):
	return render(request, "signIn.html")
	
	
def postsign(request):
	email=request.POST.get('email')
	passw = request.POST.get("pass")
	try:
		user = auth.sign_in_with_email_and_password(email,passw)
	except:
			message = "invalid cerediantials"
			return render(request,"signIn.html",{"msg":message})
	print(user)
	return render(request, "welcome.html",{"e":email})