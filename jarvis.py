import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import requests
import yagmail
import schedule
import time
from bs4 import BeautifulSoup

# Initialize the speech recognizer and text-to-speech engine
listener = sr.Recognizer()
machine = pyttsx3.init()

# Configure email
yag = yagmail.SMTP("dineshbolla21@gmail.com", "Dinesh1202")  # Replace with your email and app password

notes = []

def talk(text):
    machine.say(text)
    machine.runAndWait()

def input_instruction():
    global instruction
    try:
        with sr.Microphone() as source:
            print("Listening...")
            speech = listener.listen(source)
            instruction = listener.recognize_google(speech)
            instruction = instruction.lower()
            if "jarvis" in instruction:
                instruction = instruction.replace('jarvis', '').strip()
            print("You said:", instruction)
            return instruction
    except Exception as e:
        print(f"Error: {e}")
        return ""

def get_weather(city):
    api_key = "YOUR_API_KEY"  # Replace with your OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_desc = data['weather'][0]['description']
        temperature = data['main']['temp']
        return f"The weather in {city} is currently {weather_desc} with a temperature of {temperature}°C."
    else:
        return "Sorry, I couldn't fetch the weather information."

def send_email(recipient, subject, body):
    yag.send(to=recipient, subject=subject, contents=body)
    talk("Email has been sent.")

def take_note():
    talk("What would you like to note down?")
    note = input_instruction()
    notes.append(note)
    talk("Note saved.")

def get_notes():
    if notes:
        talk("Here are your notes:")
        for note in notes:
            print(note)  # For debugging
            talk(note)
    else:
        talk("You have no notes.")

def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.title.string if soup.title else 'No title found'
    return title

def play_Jarvis():
    instruction = input_instruction()
    if "stop" in instruction or "exit" in instruction:
        talk("Goodbye!")
        return False

    if "play" in instruction:
        song = instruction.replace('play', '').strip()
        talk("Playing " + song)
        pywhatkit.playonyt(song)

    elif 'time' in instruction:
        time_now = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time_now)

    elif 'date' in instruction:
        date_today = datetime.datetime.now().strftime('%d / %m / %Y')
        talk("Today's date is " + date_today)

    elif 'how are you' in instruction:
        talk('I am fine, how about you?')

    elif 'friday' in instruction:
        talk('Hey Boss Welcome Back.......')

    
    elif 'what is your name' in instruction:
        talk('I am Jarvis, your virtual assistant. What can I do for you?')

    elif 'who is' in instruction:
        human = instruction.replace('who is', "").strip()
        info = wikipedia.summary(human, 1)
        talk(info)

    elif 'weather in' in instruction:
        city = instruction.replace('weather in', '').strip()
        weather_info = get_weather(city)
        talk(weather_info)

    elif 'remind me to' in instruction:
        reminder = instruction.replace('remind me to', '').strip()
        schedule.every().day.at("09:00").do(lambda: talk(f"Reminder: {reminder}"))
        talk(f"I will remind you to {reminder} every day at 9 AM.")

    elif 'note' in instruction:
        if 'take' in instruction:
            take_note()
        elif 'get' in instruction:
            get_notes()

    elif 'send email to' in instruction:
        try:
            recipient = instruction.split('to ')[1].split('subject')[0].strip()
            subject = instruction.split('subject ')[1].split('body')[0].strip()
            body = instruction.split('body ')[1].strip()
            send_email(recipient, subject, body)
        except IndexError:
            talk("I couldn't understand the email details.")

    elif 'scrape' in instruction:
        url = instruction.split('scrape ')[1].strip()
        title = scrape_website(url)
        talk(f"The title of the page is: {title}")

    else:
        talk('Please repeat.')

    return True

# Main loop to keep the assistant running
while True:
    if not play_Jarvis():
        break

    # Run pending scheduled tasks
    schedule.run_pending()
    time.sleep(1)
