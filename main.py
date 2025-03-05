import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import musicplayerlibrary
import requests
import psutil
import subprocess
import random

recognizer = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')

# Set the voice (0 for male, 1 for female, depending on your system)
engine.setProperty('voice', voices[1].id)  # Female voice (can be changed to 0 for male)

# Set speech rate (speed)
engine.setProperty('rate', 150)  # Normal speech rate, adjust the value as needed

# Set volume (optional)
engine.setProperty('volume', 1)  # Volume range is from 0.0 to 1.0

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_system_info():
    battery = psutil.sensors_battery()
    battery_percent = battery.percent
    cpu_usage = psutil.cpu_percent(interval=1)
    return f"Battery: {battery_percent}% | CPU Usage: {cpu_usage}%"

def play_random_song():
    playlist = ["song1", "song2", "song3", "song4"]
    song = random.choice(playlist)
    song_url = musicplayerlibrary.music.get(song)
    if song_url:
        webbrowser.open(song_url)
        speak(f"Playing {song}.")
    else:
        speak("Sorry, I couldn't find a song to play.")

def get_joke():
    response = requests.get('https://official-joke-api.appspot.com/random_joke')
    data = response.json()
    return f"{data['setup']} - {data['punchline']}"

def processCommand(c):
    print(f"Recognized: {c}")
    speak(c)
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif c.lower().startswith("play"):
        song= c.lower().split(" ")[1]
        if song in musicplayerlibrary.music:
            link= musicplayerlibrary.music[song]
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find that song.")
            print("Song not found!")
    elif "system info" in c.lower():
        system_info = get_system_info()
        speak(system_info)
        print(system_info)
    elif "random song" in c.lower():
        play_random_song()
    elif "tell me a joke" in c.lower():
        joke = get_joke()
        speak(joke)
        print(joke)
    else:
        speak("I didn't quite understand that command.")
       

if __name__ == "__main__":
    speak("Initializing jarvis...")
    while True:
        r = sr.Recognizer()
        print("recognizing....")
        try:
            with sr.Microphone() as source:
                print("Listening....")
                audio = r.listen(source,timeout=2,phrase_time_limit=2)

            word = r.recognize_google(audio)
            if(word.lower()=="jarvis"):
                speak("yes, how can I help you?")
                print("yes, how can I help you?")
                with sr.Microphone() as source:
                     print("jarvis Activating....")
                     audio = r.listen(source,timeout=2)
                     command = r.recognize_google(audio)
                     
                     processCommand(command)
        
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand the audio.")
            speak("Sorry, I couldn't understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            speak("Could not request results from Google Speech Recognition service")
        except Exception as e:
            print(" Error; {0}".format(e))

