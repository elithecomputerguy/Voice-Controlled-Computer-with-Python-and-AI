#!/usr/bin/env python3

import speech_recognition as sr
from gtts import gTTS 
import os 
from datetime import datetime
import requests
import serial

import openai

openai.api_key = 'APIKEY'

r = sr.Recognizer()
language = 'en'

#For serial connection Google for your OS. /dev/cu. is for Mac Os.  /dev/ttyACM0 is for Ubuntu
ser = serial.Serial('/dev/cu.usbmodem14101',9600, timeout=1)
ser.flush()

def get_time():
    current_time = datetime.now()
    message = str(current_time.strftime("%A %H:%M"))
    return message

def get_weather():
    ip_address = requests.get('https://api.ipify.org').text	
    ip_data = requests.get(f'http://ip-api.com/json/{ip_address}').json()
    weather = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={ip_data["lat"]}&lon={ip_data["lon"]}&units=imperial&appid=APIKEY').json()
    message = f'{weather["main"]["temp"]} degrees'
    return message

def get_joke(phrase):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "you are a comedian"},
        {"role": "assistant", "content": "answer in less than 25 words"},
        {"role": "user", "content": phrase}
        ]
    )
    message = response["choices"][0]["message"]["content"]
    return message

def switch_light(phrase):
    if 'on' in phrase:
        try:
            ser.write(b"on\n")
            message = 'Light is On'
        except:
            pass
    elif 'off' in phrase:
        try:
            ser.write(b"off\n")
            message = 'Light is Off'
        except:
            pass
    else:
        message = 'I dont understand what to do with the light'

    return message

while True:
    response = ''
    phrase = ''
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    try:
        phrase = r.recognize_google(audio).lower()
        print(phrase)
    except sr.UnknownValueError:
        print("I do not understand")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    if "computer" in phrase:
        if 'time' in phrase:
            response = get_time()
        elif 'weather' in phrase:
            response = get_weather()
        elif 'joke' in phrase:
            response = get_joke(phrase)
        elif 'light' in phrase:
            response = switch_light(phrase)
        elif 'dismissed' in phrase:
            break
        else:
            pass

        print(response)

        try:
            myobj = gTTS(text=response, lang=language, slow=False) 

            myobj.save("response.mp3") 

            os.system("afplay response.mp3") 
        except:
            pass