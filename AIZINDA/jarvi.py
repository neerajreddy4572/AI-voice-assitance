import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import requests
import math


# Initialize pyttsx3 engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Function to speak out the given audio
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to wish the user based on the time of the day
def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")   
    else:
        speak("Good Evening!")  
    speak("I am Jarvis, Sir. Please tell me how may I help you.")       


def getJoke():
    # API endpoint for fetching jokes
    joke_api_url = "https://official-joke-api.appspot.com/jokes/random"
    
    try:
        # Send a GET request to the joke API
        response = requests.get(joke_api_url)
        # Parse the JSON response
        joke_data = response.json()
        
        # Extract the setup and punchline of the joke
        setup = joke_data["setup"]
        punchline = joke_data["punchline"]
        
        # Combine setup and punchline to form the complete joke
        joke = f"{setup}\n{punchline}"
        return joke
    except Exception as e:
        return "Sorry, I couldn't fetch a joke at the moment."

# Function to take voice commands from the user
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again, please...")  
        return "None"
    return query.lower()

# Function to get weather forecast for a city
def getWeatherForecast(city):
    # API key for OpenWeatherMap
    api_key = "58a3894abad8ee60c8adb60ff71b4126"
    # API endpoint for current weather data
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        # Request weather data from the API
        response = requests.get(url)
        # Extract JSON data
        data = response.json()
        
        if data["cod"] == 200:
            # Extract relevant weather information
            weather_desc = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            
            # Speak out the weather forecast
            speak(f"The weather in {city} is {weather_desc}.")
            speak(f"The temperature is {temperature} degrees Celsius, with humidity at {humidity} percent.")
            speak(f"The wind speed is {wind_speed} meters per second.")
        else:
            speak("Sorry, I couldn't retrieve the weather information for that location.")
    except Exception as e:
        print("An error occurred:", e)

def evaluateExpression(expression):
    try:
        result = eval(expression)
        speak(f"The result is {result}")
    except Exception as e:
        speak("Sorry, I couldn't calculate the result.")

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")

        elif 'open google' in query:
            webbrowser.open("https://www.google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("https://www.stackoverflow.com")   

        elif "what's the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            codePath = "C:\\Users\\neera\\Desktop\\AIZINDA\\jarvis.py"
            os.startfile(codePath)
        
        elif 'play music' in query:
            # Implement music playing functionality
            pass

        elif 'weather forecast' in query:
            # Extract city name from user's query
            city = query.split("for")[-1].strip()
            getWeatherForecast(city)
        
        elif 'exit' in query:
            speak("Goodbye, Sir!")
            break
        elif 'calculate' in query:
            # Extract the expression to be evaluated
            expression = query.split("calculate")[-1].strip()
            evaluateExpression(expression)
        
        elif 'tell me a joke' in query:
           joke = getJoke()
           speak(joke)