import pyaudio
import wave
import googletrans
import speech_recognition
import gtts
import pyttsx3


def SpeakText(command):
    
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-50)


def record_audio():
    # Initialize pyaudio
    p = pyaudio.PyAudio()

    # Open a stream to record from the laptop speaker
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

    # Start recording
    audio = []
    for i in range(0, int(44100 / 1024 * 5)):
        data = stream.read(1024)
        audio.append(data)

    # Stop recording
    stream.stop_stream()
    stream.close()

    # Return the audio data
    return audio


def translate_audio(audio):
    # Convert audio to text using Google Translate
    translator = googletrans.Translator()
    text = translator.translate(audio, dest="en")
    return text


def save_audio(audio, filename):
    # Save audio to file
    converted_audio = gtts.gTTS(text, lang="en")
    converted_audio.save(filename)


if __name__ == "__main__":
    # Record audio from laptop speaker
    audio = record_audio()

    # Convert audio to text using Google Translate
    text = translate_audio(audio)

    # Save audio to file
    save_audio(text, "output.mp3")

    # Speak the translated text
    SpeakText(text)
