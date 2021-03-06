from django.shortcuts import render
from django.contrib import auth  # for log out
import pyrebase
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.http import JsonResponse
from itertools import islice
import struct

# twitter stuff
import os
from twython import Twython
import base64
import uuid
from datetime import datetime
from .t import (
    ACCESS_TOKEN_KEY,
    ACCESS_TOKEN_SECRET,
    CONSUMER_KEY,
    CONSUMER_SECRET,
)

twitter = Twython(
    CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET
)
from PIL import Image
import requests
from io import BytesIO
import socket
import json

config = {
    "apiKey": "AIzaSyAhaOe24nDVf_6PRgjfffu1PwQss2QI3I4",
    "authDomain": "fishbowl-c47d5.firebaseapp.com",
    "databaseURL": "https://fishbowl-c47d5.firebaseio.com",
    "projectId": "fishbowl-c47d5",
    "storageBucket": "fishbowl-c47d5.appspot.com",
    "messagingSenderId": "230121294113",
}


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()
storage = firebase.storage()

TCP_IP = "0.0.0.0"
TCP_PORT = 5000

# Routing functions
def singIn(request):
    return render(request, "signIn.html")


def postsign(request):
    email = request.POST.get("email")
    passw = request.POST.get("pass")
    try:
        user = auth.sign_in_with_email_and_password(email, passw)
    except:
        message = "invalid cerediantials"
        return render(request, "signIn.html", {"msg": message})
    print(user["idToken"])
    session_id = user["idToken"]
    request.session["uid"] = str(session_id)
    return render(request, "welcome.html", {"e": email})


def logout(request):
    return render(request, "signIn.html")


def signUp(request):

    return render(request, "signup.html")


def postsignup(request):

    name = request.POST.get("name")
    email = request.POST.get("email")
    passw = request.POST.get("pass")
    try:
        user = auth.create_user_with_email_and_password(email, passw)
        uid = user["localId"]
        data = {"name": name, "status": "1"}
        database.child("users").child(uid).child("details").set(data)
    except:
        message = "Unable to create account try again"
        return render(request, "signup.html", {"messg": message})

    return render(request, "signIn.html")


def create(request):

    return render(request, "create.html")


def post_create(request):

    temp = request.POST.get("temp")
    ph = request.POST.get("ph")

    idtoken = request.session["uid"]
    a = auth.get_account_info(idtoken)
    a = a["users"]
    a = a[0]
    a = a["localId"]
    print("info" + str(a))
    data = {"temperature": temp, "ph": ph}
    database.child("users").child(a).child("reports").set(data)
    name = (
        database.child("users")
        .child(a)
        .child("details")
        .child("name")
        .get()
        .val()
    )
    return render(request, "welcome.html", {"e": name})


def post_check(request):

    idtoken = request.session["uid"]
    a = auth.get_account_info(idtoken)
    a = a["users"]
    a = a[0]
    a = a["localId"]

    temp = (
        database.child("users")
        .child(a)
        .child("reports")
        .child("temperature")
        .get()
        .val()
    )
    ph = (
        database.child("users")
        .child(a)
        .child("reports")
        .child("ph")
        .get()
        .val()
    )

    name = (
        database.child("users")
        .child(a)
        .child("details")
        .child("name")
        .get()
        .val()
    )

    return render(request, "post_check.html", {"t": temp, "p": ph, "e": name})


def fetch_data(request):
    email = "yunzhuyang97@yeah.net"
    passw = "333666"
    user = auth.sign_in_with_email_and_password(email, passw)
    a = user["localId"]
    print(a)
    ph = (
        database.child("users")
        .child(a)
        .child("reports")
        .child("ph")
        .get()
        .val()
    )
    temp = (
        database.child("users")
        .child(a)
        .child("reports")
        .child("temperature")
        .get()
        .val()
    )

    data = {"temperature": temp, "ph": ph}

    return JsonResponse(data)


def temp(request):
    temps = database.child("temp").get()
    temps = islice(temps.each(), 10)
    data = []
    for temp in temps:
        print(temp.val())
        data.append(temp.val())
    return JsonResponse(data, safe=False)


def ph(request):
    phs = database.child("ph").get()
    phs = islice(phs.each(), 10)
    data = []
    for ph in phs:
        print(ph.val())
        data.append(ph.val())
    return JsonResponse(data, safe=False)


def feed(request):
    database.child("feed").set(True)
    data = {"response": "success"}
    return JsonResponse(data, safe=False)


@csrf_exempt
def tweet_something(request):
    id = request.POST.get("id")
    msg = request.POST.get("msg")
    try:
        # fetch base64 string from firebase based on picture id
        print(id)
        base64str = database.child("/images/" + id + "/data").get().val()
        imgdata = base64.b64decode(base64str)

        # save the image with a unique file name
        unique_filename = str(uuid.uuid4())
        with open(unique_filename, "wb") as f:
            f.write(imgdata)
        img = open(unique_filename, "rb")

        # tweet that image with message and remove it 
        tweet(msg, img)
        os.remove(unique_filename)

        data = {"response": "success"}
        return JsonResponse(data, safe=False)
    except Exception as e:
        data = {"response": "fail: " + str(e)}
        return JsonResponse(data, safe=False)


def stream(request):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(True)
    conn, addr = s.accept()

    data = recv_msg(conn)
    s.close()
    json_data = json.dumps(str(data))
    return JsonResponse(json_data, safe=False)


@csrf_exempt
def snapshot(request):
    try:
        # make a new json object with the base64 string, current timestamp, and
        # picture id
        base64_string = request.POST.get("data")
        upload_time = datetime.utcnow().isoformat()
        new_img_ref = database.child("images").push(
            {"id": "", "data": "", "timestamp": ""}
        )
        id = new_img_ref["name"]

        # add a new entry to the firebase/images
        database.child("images").child(id).update(
            {"id": id, "data": base64_string, "timestamp": upload_time}
        )
        data = {"response": "success"}
        return JsonResponse(data, safe=False)
    except Exception as e:
        data = {"response": "fail: " + str(e)}
        return JsonResponse(data, safe=False)


# Normal functions

# send a tweet with a message and an image
def tweet(msg, img):
    response = twitter.upload_media(media=img)
    media_id = [response["media_id"]]
    twitter.update_status(status=msg, media_ids=media_id)
    print("Tweeted: %s" % msg)


def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack(">I", raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)


def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b""
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data
