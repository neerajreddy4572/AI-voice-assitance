import pyttsx3
import speech_recognition as sr
from google.cloud import translate_v2 as translate
import datetime
import wikipedia
import webbrowser
import os
import requests
import math
import random
import requests
from googleapiclient.discovery import build


# Initialize pyttsx3 engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Function to search and fetch information from Wikipedia
def searchWikipedia(query):
    try:
        # Search Wikipedia for the query
        search_results = wikipedia.search(query)
        
        if search_results:
            # Fetch the summary of the first search result
            page_summary = wikipedia.summary(search_results[0], sentences=2)
            return page_summary
        else:
            return "Sorry, I couldn't find information on that topic."
    except wikipedia.exceptions.DisambiguationError as e:
        # Handle disambiguation error (multiple possible meanings)
        return f"Multiple results found. Can you be more specific?"
    except wikipedia.exceptions.PageError as e:
        # Handle page not found error
        return "Sorry, I couldn't find information on that topic."


# Function to fetch a random joke
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
# def getWeatherForecast(city):
#     # API key for OpenWeatherMap
#     api_key = "58a3894abad8ee60c8adb60ff71b4126"
#     # API endpoint for current weather data
#     url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
#     try:
#         # Request weather data from the API
#         response = requests.get(url)
#         # Extract JSON data
#         data = response.json()
        
#         if data["cod"] == 200:
#             # Extract relevant weather information
#             weather_desc = data["weather"][0]["description"]
#             temperature = data["main"]["temp"]
#             humidity = data["main"]["humidity"]
#             wind_speed = data["wind"]["speed"]
            
#             # Speak out the weather forecast
#             speak(f"The weather in {city} is {weather_desc}.")
#             speak(f"The temperature is {temperature} degrees Celsius, with humidity at {humidity} percent.")
#             speak(f"The wind speed is {wind_speed} meters per second.")
#         else:
#             speak("Sorry, I couldn't retrieve the weather information for that location.")
#     except Exception as e:
#         print("An error occurred:", e)

def evaluateExpression(expression):
    try:
        result = eval(expression)
        speak(f"The result is {result}")
    except Exception as e:
        speak("Sorry, I couldn't calculate the result.")




# Function to look up word definitions, synonyms, antonyms, example sentences, and pronunciation
def lookupWord(word):
    try:
        # API endpoint for word lookup
        api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        
        # Send a GET request to the API
        response = requests.get(api_url)
        data = response.json()
        
        
        # Extract relevant information from the API response
        if isinstance(data, list):
            word_data = data[0]
            meanings = word_data.get("meanings", [])
            
            # Construct the response message
            response_msg = f"Definitions of {word}:\n"
            for meaning in meanings:
                definition = meaning.get("definition", "N/A")
                part_of_speech = meaning.get("partOfSpeech", "N/A")
                response_msg += f"{part_of_speech}: {definition}\n"
                
                # Get usage examples
                examples = meaning.get("examples", [])
                if examples:
                    response_msg += "Examples:\n"
                    for example in examples:
                        response_msg += f"- {example}\n"
            
            # Get pronunciation guide
            pronunciation = word_data.get("phonetics", [])
            if pronunciation:
                response_msg += f"\nPronunciation: {pronunciation[0]['text']}"
            
            return response_msg
        else:
            return "Sorry, I couldn't find any information for that word."
    except Exception as e:
        return "Sorry, I couldn't look up the word at the moment."



#speach transulation

# Function to recognize and translate speech
def translate_speech():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        # Recognize speech and detect language
        text = recognizer.recognize_google(audio, language='en')
        source_language = translator.detect_language(text)

        # Translate text to target language (e.g., French)
        translation = translator.translate(text, target_language='fr')

        print(f"Original text: {text}")
        print(f"Translated text: {translation['translatedText']}")

        # Speak out the translated text
        engine.say(translation['translatedText'])
        engine.runAndWait()

    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the audio.")
    except sr.RequestError as e:
        print("Sorry, there was an error while processing the audio request:", e)

# Function to handle user commands
def handle_command(command):
    if 'translate' in command:
        translate_speech()
    # Add other command handling logic here









if __name__ == "__main__":

    
    wishMe()
    while True:
        user_input = input("Enter a command: ").lower()
        handle_command(user_input)
        query = takeCommand()

        # if 'wikipedia' in query:
        #     speak('Searching Wikipedia...')
        #     query = query.replace("wikipedia", "")
        #     results = wikipedia.summary(query, sentences=2)
        #     speak("According to Wikipedia")
        #     print(results)
        #     speak(results)
        if 'define' in query:
            word = query.split("define")[1].strip()
            definition = lookupWord(word)
            speak(definition)


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
        
        # elif 'play music' in query:
        #     # Implement music playing functionality
        #     pass

        elif 'search Wikipedia for' in query:
            search_query = query.split("search Wikipedia for")[1].strip()
            wikipedia_summary = searchWikipedia(search_query)
            speak(wikipedia_summary)

        # elif 'weather forecast' in query:
        #     # Extract city name from user's query
        #     city = query.split("for")[-1].strip()
        #     getWeatherForecast(city)
        
        elif 'exit' in query:
            speak("Goodbye, Sir!")
            break
        elif 'calculate' in query:
            # Extract the expression to be evaluated
            expression = query.split("calculate")[-1].strip()
            evaluateExpression(expression)
        elif 'say my name' in query:
            speak("Your name is G NEERAJ REDDY.")  # Replace [Your Name] with your actual name

        elif "say my teammates names" in query:
            speak("Your teammtes names are  likhith and Abhiram.")  # Replace [Your Name] with your actual name
        
        elif 'tell me a joke' in query:
           joke = getJoke()
           speak(joke)
       
        
