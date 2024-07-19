import googletrans
import speech_recognition
import gtts
import pyttsx3
# import pyaudio

#audio_file = speech_recognition.AudioFile("audio_file.wav")
def SpeakText(command):
    
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-50)

print("Speak now...")
lang="hi"
x=0
while(x<1000):
    recognizer = speech_recognition.Recognizer()
    # with audio_file as source:
    with speech_recognition.Microphone() as source:
        audio = recognizer.listen(source)
        text = recognizer.recognize_google(audio, language="en-us")

    translator = googletrans.Translator()
    translation = translator.translate(text, dest=lang)
    print( translation.text)
    converted_audio = gtts.gTTS(translation.text, lang=lang)
    SpeakText(translation.text)
    x=x+1
