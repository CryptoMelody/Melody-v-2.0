#MELODY Current Version is 2.0 
#Warning: For this code use Python version 3.13 and lower, cause of the library "pygame"!!! 
import pygame
import time
import os
import webbrowser
import json
import pyaudio
import urllib.parse
from vosk import Model, KaldiRecognizer
from openai import OpenAI
import pyttsx3 
pygame.mixer.init()
#CHAT-GPT:
client = OpenAI (
    base_url = "https://openrouter.ai/api/v1",
    api_key = "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"
    )

model = Model(r"D:\Voices\vosk-model-small-en-us-0.15")
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

def google_search(query):
    search_url = f"https://www.google.com/search?q={query}"
    search_url = search_url.replace(' ', '+')
    webbrowser.open(search_url)

def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if (rec.AcceptWaveform(data)) and (len(data) > 0):
            answer = json.loads(rec.Result())
            if answer['text']:
                yield answer['text']

def play_sound(file_path):
  
    try:
        
        if not os.path.exists(file_path):
            print(f"Audio file not found: {file_path}")
            return False
        
      
        try:
        
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            return True
        except pygame.error:
        
            try:
                sound = pygame.mixer.Sound(file_path)
                sound.play()
                time.sleep(sound.get_length() + 0.5)
                return True
            except:
                
                print(f"Using system player for: {file_path}")
                os.system(f'start "" "{file_path}"')
                time.sleep(2)  
                return True
                
    except Exception as e:
        print(f"Error playing sound {file_path}: {e}")
        return False

def process_command(command):
    #OPTIMIZED
    if command.lower().startswith('find'):
        site = None
        site_name = command[5:].strip()
        if site_name == "yandex" or site_name == "andex":
            site = 'https://yandex.com'
        elif site_name == "youtube" or site_name == "you tube":
            site = 'https://youtube.com'
        elif site_name == "the mail" or site_name == "ail":
            site = 'https://mail.ru'
        
        if site:
            play_sound(r"D:\Voices\33.wav")
            webbrowser.open(site)
        else:
            print(f"Unknown site: {site_name}")
            
    elif command.lower().startswith('search'):
        p = command[6:].strip()
        play_sound(r"D:\Voices\53.wav")
        google_search(p)
        
    elif command.lower().startswith('open'):
        p = command[5:].strip()
        if p == "browser":
            os.system(f"start browser.exe")
            play_sound(r"D:\Voices\16.wav")
        else:
            play_sound(r"D:\Voices\2.wav")
            print('Unknown programm')

    #CHAT-GPT:
    elif command.lower().startswith("melody"):
        melody = True 
        p = command[7:].strip()
        completion = client.chat.completions.create (
            model = "qwen/qwen3-vl-235b-a22b-thinking",
            messages = [
        {"role": "system", 
         "content": "Speak like a friend" 
         },                                 
        {"role": "user",
         "content": p
         },
      ],
            )
        #TTS-model
        engine = pyttsx3.init()
        voices = engine.getProperty("voices")
        engine.setProperty("voice", voices[1].id)
        engine.say(completion.choices[0].message.content)
        engine.runAndWait()
        
        
for text in listen():
    print(f"Recognized: {text}")
    #OPTIMIZED
    if text.lower() == "thanks" or text.lower() == "thank you":
        play_sound(r"D:\Voices\54.wav")
    elif text.lower() == "hello" or text.lower() == "ello":
        play_sound(r"D:\Voices\35.wav")
    elif text.lower() == "you are an asshole":
        play_sound(r"D:\Voices\37.wav")
    elif text.lower() == "i did that":
        play_sound(r"D:\Voices\10.wav")
    else:
      process_command(text)
