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

from .forms import CatForm, LoginForm, SignUpForm, ToyForm, UploadPicture




from .models import Cat, Toy, Picture

BUCKET_NAME = 'chelsea-motion-detector'
S3_BUCKET = 's3://{}/'.format(BUCKET_NAME)

def index(request):
    return render(request, 'index.html')

def profile(request, username):
    user = User.objects.get(username=username)
    cats = Cat.objects.filter(user=user)
    return render(request, 'profile.html', {'username': username, 'cats': cats})


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
                    return HttpResponseRedirect('/')
                else:
                    print("The account has been disabled.")
            else:
                print("The username and/or password is incorrect.")
                return HttpResponseRedirect('/')
                
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')



def api(request):
    payload = {'key': 'Mjk0MTkz'}
    res = requests.get('http://thecatapi.com/api/images/get', params=payload)
    return render(request, 'api.html', {'imageurl': res.url})


def read_file_as_byte64(client, s3_location):
    """
    Read s3location (s3://xxxx) as images which can be
    shown on web

    Args:
        client (boto3.client): The s3 client
        s3_location (str): "s3://xxx"-like s3 location

    Returns:
        str: The byte64 string for images

    References:
        https://stackoverflow.com/questions/20756042/javascript-how-to-display-image-from-byte-array-using-javascript-or-servlet

    """
    s3_loc_split = s3_location.split("/")
    bucket = s3_loc_split[2]
    s3_file = '/'.join(s3_loc_split[3:])
    return "data:image/png;base64," + base64.encodestring(
        client.get_object(Bucket=bucket, Key=s3_file)['Body'].read()
    ).decode("utf-8")


def motion_result(request):
    # using UploadPicture Form, see line 192
    form = UploadPicture()

    if request.method == 'POST':
        # read the uploaded image
        image_bytes = request.FILES['image'].read()
        # build a connection to s3, permission needed, it will read envirn variables
        s3_client = boto3.client('s3', region_name='us-west-2')

        username = request.user.get_username()

        #UUID4() generates a unique ID with higher security than UUID1()
        identify_key = uuid.uuid4()
        s3_key = "{}/{}".format(username, identify_key)
        # uploading file to bucket 'chelsea-motion-dectector'

        s3_client.upload_fileobj(
            BytesIO(image_bytes),
            BUCKET_NAME,
            s3_key)

        rekognition_client = boto3.client('rekognition', region_name='us-west-2')
        rekoginition_response = rekognition_client.detect_faces(
            Image={'Bytes': image_bytes},
            Attributes=['ALL']
        )
        # Find out the max matching mood from api
        mood = max(rekoginition_response['FaceDetails'][0]['Emotions'],
            key=lambda x: x['Confidence'])['Type']

        #save the info about this picture to DB
        new_image_record = Picture.objects.create(
            user=request.user,
            mood=str(mood),
            name= S3_BUCKET + s3_key
        )
        new_image_record.save()
        img_bytes_string = base64.encodestring(
            image_bytes).decode(
            "utf-8")
        return render(request, 'motion_result.html',
                  {'result': str(mood), 'form': form,
                   'img': "data:image/png;base64," + img_bytes_string})



    # if this is a get request, show the picture upload form
    return render(request, 'motion_result.html',
                  {'result': "Unknown", 'form': form, 'img': ""})

#-----------------------------------------------chart
from django.views.generic import TemplateView
from django.contrib.auth.models import User

def chart(request):
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
    #find all picture records of the user who is logged in
    picture_records = Picture.objects.filter(user=request.user)
    image_array = []
    #establish client with AWS
    s3_client = boto3.client('s3')

    for picture_object in picture_records:
        image_array.append({
            "mood": picture_object.mood,
            "timestamp": picture_object.timestamp,
            "img": read_file_as_byte64(s3_client, picture_object.name)
        })

    return render(request, 'history.html', {'pictures': image_array})

def gallery(request):
    #find all picture records of the user who is logged in
    picture_records = Picture.objects.filter(user=request.user)[:10]
    image_array = []
    #establish client with AWS
    s3_client = boto3.client('s3')

    for picture_object in picture_records:
        image_array.append({
            "mood": picture_object.mood,
            "timestamp": picture_object.timestamp,
            "img": read_file_as_byte64(s3_client, picture_object.name)
        })

    return render(request, 'gallery.html', {'pictures': image_array})

def sample(request):
    return render(request, 'sample.html')
