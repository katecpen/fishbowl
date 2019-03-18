from django.shortcuts import render 
from django.contrib import auth    #for log out
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
database=firebase.database()	
	
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
	print(user['idToken'])
	session_id=user['idToken']
	request.session['uid']=str(session_id)
	return render(request, "welcome.html",{"e":email})
def logout(request):
    return render(request, "signIn.html")
def signUp(request):

    return render(request,"signup.html")
def postsignup(request):

    name=request.POST.get('name')
    email=request.POST.get('email')
    passw=request.POST.get('pass')
    try:
        user=auth.create_user_with_email_and_password(email,passw)
        uid = user['localId']
        data={"name":name,"status":"1"}
        database.child("users").child(uid).child("details").set(data)
    except:
        message="Unable to create account try again"
        return render(request,"signup.html",{"messg":message})
        

    
    return render(request,"signIn.html")	
def create(request):

    return render(request,'create.html')


def post_create(request):

  
    temp = request.POST.get('temp')
    ph =request.POST.get('ph')

    idtoken= request.session['uid']
    a = auth.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    print("info"+str(a))
    data = {
        "temperature":temp,
        'ph':ph
    }
    database.child('users').child(a).child('reports').set(data)
    name = database.child('users').child(a).child('details').child('name').get().val()
    return render(request,'welcome.html', {'e':name})	

def post_check(request):

    

    idtoken = request.session['uid']
    a = auth.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    temp =database.child('users').child(a).child('reports').child('temperature').get().val()
    ph =database.child('users').child(a).child('reports').child('ph').get().val()
    
    name = database.child('users').child(a).child('details').child('name').get().val()

    return render(request,'post_check.html',{'t':temp,'p':ph,'e':name})
