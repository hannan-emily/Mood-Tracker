"""
The :mod: `views` is to give all possible routable actions
for all pages
"""

# Author: Emily Hannan & Chelsea Zhu
# License: MIT License

import boto3
import base64
import uuid
import warnings
import requests
import logging
import json

from io import BytesIO
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
# we add redirect with auth
from django.contrib.auth import authenticate, login, logout, authenticate

from .forms import LoginForm, SignUpForm, UploadPicture
from .models import Picture

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        # if post, then authenticate (user submitted username and password)
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username=u, password=p)
            if user is not None:
                if user. is_active:
                    login(request, user)
                    # return HttpResponseRedirect('/')
                    return redirect('/sample')
                else:
                    print("The account has been disabled.")
            else:
                print("The username and/or password is incorrect.")
                # return HttpResponseRedirect('/')
                form = LoginForm()
                return render(request, 'login.html', {'form': form, 'msg': 'Incorrect credentials, please try again.'})

    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form, 'msg': ''})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

#To reduce the number requests on the server, embed some images (PNG & SVG) as BASE64 directly into the css. 
def img_base64_encoding(img_bytes):
     return "data:image/png;base64," + base64.encodestring(
        img_bytes).decode("utf-8")


def motion_result(request):
    if str(request.user) == 'AnonymousUser':
        return redirect('/login')
    else:
        form = UploadPicture()

        if request.method == 'POST':
            # read the uploaded image
            image_bytes = request.FILES['image'].read()

            username = request.user.get_username()

            img_encoding = img_base64_encoding(image_bytes)
            try:
                rekognition_client = boto3.client('rekognition', region_name='us-west-2')
                rekoginition_response = rekognition_client.detect_faces(
                    Image={'Bytes': image_bytes},
                    Attributes=['ALL']
                )
            # Find out the max matching mood from api
                mood = max(rekoginition_response['FaceDetails'][0]['Emotions'],
                    key=lambda x: x['Confidence'])['Type']
                new_image_record = Picture.objects.create(
                    user=request.user,
                    mood=str(mood),
                    name= img_encoding
                )
                new_image_record.save()
            except Exception as error:
                print(error)
                mood = "Unknown"
            #save the info about this picture to DB

            return render(request, 'motion_result.html',
                      {'result': str(mood), 'form': form,
                       'img': img_encoding})



    # if this is a get request, show the picture upload form
    return render(request, 'motion_result.html',
                  {'result': "Unknown", 'form': form, 'img': ""})

# -----------------------------------------------chart
from django.views.generic import TemplateView
from django.contrib.auth.models import User

def chart(request):
    if str(request.user) == 'AnonymousUser':
        return redirect('/login')
    else:
        picture_records = Picture.objects.filter(user=request.user)
        mood_array = []
        for picture_object in picture_records:
            mood_array.append(picture_object.mood)
        unique_mood = list(set(mood_array))
        dd = {}
        for mood in unique_mood:
            dd[mood] = mood_array.count(mood)

        return render(request, 'chart.html', {'graph_labels': list(dd.keys()), 'graph_values': list(dd.values())})


def history(request):
    if str(request.user) == 'AnonymousUser':
        return redirect('/login')
    else:
        #find all picture records of the user who is logged in
        picture_records = Picture.objects.filter(user=request.user)
        image_array = []
        #establish client with AWS

        for picture_object in picture_records:
            image_array.append({
                "mood": picture_object.mood,
                "timestamp": picture_object.timestamp,
                "img": picture_object.name
            })

        return render(request, 'history.html', {'pictures': image_array})

def gallery(request):
    if str(request.user) == 'AnonymousUser':
        return redirect('/login')
    else:
        #find all picture records of the user who is logged in
        picture_records = Picture.objects.filter(user=request.user)[:10]
        image_array = []
        #establish client with AWS

        for picture_object in picture_records:
            image_array.append({
                "id": picture_object.id,
                "mood": picture_object.mood,
                "timestamp": picture_object.timestamp,
                "img": picture_object.name
            })

        if str(request.user) == 'AnonymousUser':
            return redirect('/login')
        else:
            picture_records = Picture.objects.filter(user=request.user)
            mood_array = []
            for picture_object in picture_records:
                mood_array.append(picture_object.mood)
            unique_mood = list(set(mood_array))
            dd = {}
            for mood in unique_mood:
                dd[mood] = mood_array.count(mood)

        return render(request, 'gallery.html', {'pictures': image_array, 'graph_labels': list(dd.keys()), 'graph_values': list(dd.values())})




def sample(request):
    return render(request, 'sample.html')

def about(request):
    return render(request, 'about.html')
