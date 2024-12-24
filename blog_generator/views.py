from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from pytube import YouTube
from django.conf import settings
import os 
import speech_recognition as sr
import pafy

@login_required
def index(request):
    return render(request, 'index.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username = username, password = password)
        
        if user is not None:
            login(request, user)
            return redirect("/")
        
        else: 
            error_message = "User does not matched"
            return render(request, 'login.html', {'error_message':error_message})
        
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeatPassword = request.POST['repeatPassword']
        
        if password == repeatPassword:
            try: 
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return redirect('/')
            except Exception as e:
                error_message = f"Error creating account :{e}"   
                return render(request, 'signup.html', {'error_message':error_message})
                
        else:
            error_message = "Password do not match"
            return render(request, 'signup.html', {'error_message': error_message})
        
    return render(request, 'signup.html')

def user_logout(request):
    
    logout(request)
    return redirect('/')
    
@csrf_exempt
def generate_blog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("data", data)
            yt_link = data['link']
        
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid data sent'}, status = 400)
        
        # yt_title_value  = yt_title(yt_link)
        
        transcription = get_transcription(yt_link)
        
        if not transcription : 
            return JsonResponse({'error':'failed to load'}, status = 500)
        
        
        return JsonResponse({'content' : transcription})

    else: 
        return JsonResponse({'error': "Invalid request method"}, status = 405)
    

def download_audio(link):
  
    try:
        # Create a new video object from the URL
        video = pafy.new(link)
        
        # Get the best available audio stream
        bestaudio = video.getbestaudio()
        
        # Download the audio stream
        print(f"Downloading audio: {bestaudio.title}")
        filepath = bestaudio.download()
        print(f"Audio downloaded to: {filepath}")
        
        return filepath
    except Exception as e:
        print(f"Error downloading audio: {e}")
        return None 
    
def get_transcription(link):
    audio_file = download_audio(link)
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source : 
        audio = recognizer.record(source)
        
    text = recognizer.recognize_google(audio)
    print("text", text)
    return text
    
    
    
def yt_title(title):
    yt = YouTube(title)
    title = yt.title 
    
    return title