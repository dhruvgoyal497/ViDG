from django.shortcuts import render
from django.http import JsonResponse
from agora_token_builder import RtcTokenBuilder
import random
import time
import json
# modules for translation
import googletrans
import speech_recognition
import gtts
import pyttsx3

from .models import RoomMember

from django.views.decorators.csrf import csrf_exempt 
# Create your views here.

def getToken(request):
    appId = '8c88c7326fb445ba91824c4b62849e4a'
    appCertificate = '1d924e270a7849f7954f40c823ca46d7'
    channelName = request.GET.get('channel')
    uid = random.randint(1,250)
    expirationTimeInSeconds = 3600*24  #valid for one day
    currentTimeStamp = time.time()
    role = 1
    privilegeExpiredTs=currentTimeStamp + expirationTimeInSeconds
    
    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return JsonResponse({'token':token, 'uid':uid}, safe=False)

def lobby(request):
    return render(request, 'base/lobby.html')

def room(request):
    return render(request, 'base/room.html')

@csrf_exempt
def createMember(request):
    data = json.loads(request.body)

    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    return JsonResponse({'name':data['name']}, safe=False)

def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )

    name = member.name
    return JsonResponse({'name':member.name},safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)

    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name'],
    )
    member.delete()
    return JsonResponse('Member was deleted', safe=False)

# translation code


def SpeakText(command):
     
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-80)

print("Speak now...")

def translate_language(lan):
    
    x = 0
    out = str(lan)
    while x < 1000:
        recognizer = speech_recognition.Recognizer()
        with speech_recognition.Microphone() as source:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio, language=out)
        translator = googletrans.Translator()
        translation = translator.translate(text, dest="fr")
        print(translation.text)
        converted_audio = gtts.gTTS(translation.text, lang="fr")
        SpeakText(translation.text)
        x = x + 1

        

def translate(request):
    
    language = request.GET.get("language")
    print(language)
    translate_language(language)
    return render(request, 'room.html')
    