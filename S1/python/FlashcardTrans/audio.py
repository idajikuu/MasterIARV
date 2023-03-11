# -*- coding: utf-8 -*-
import speech_recognition as sr
import gtts
from playsound import playsound
import os

r = sr.Recognizer()
def getAudio():
    with sr.Microphone() as source:
        print("What's on your mind?")
        audio = r.listen(source)
    return audio

def audioToText(audio):
    text = ""
    try:
        text = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio")
    except sr.RequestError:
        print("could not request results from API")
    return text
def playSound(text):
    try:
        tts = gtts.gTTS(text)
        tempfile = "./temp.mp3"
        tts.save(tempfile)
        playsound(tempfile)
        os.remove(tempfile)
    except AssertionError:
        print("could not play sound")
        
if __name__ == "__main__":
    playSound("give me the name of the flashcard?")
    a = getAudio()
    convert = audioToText(a)
    print(convert)
    
