import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install SpeechRecognizer
import datetime
import wikipedia #pip install wikipedia
import webbrowser
import os
import smtplib # for email send
import cv2 #pip install opencv-python
import winsound
from email.message import EmailMessage
import pywhatkit #pip install pywhatkit
# from translate import Translator #pip install translator



engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


# Time section =====================================================>
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour <= 5 or hour >= 20:
        speak("Good Night sir !")

    elif 6 <= hour < 12:
        speak("Good Morning sir !")

    elif 12 <= hour < 16:
        speak("Good Afternoon sir !")

    elif 16 <= hour < 20:
        speak("Good Evening sir !")

    else:
        speak("Good Evening sir !")
# Time section =====================================================>


# Listening and Recognizing section ================================= >

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
        print("Say that again please...")
        return "Not matched with system"
    return query

# Listening and Recognizing section ================================= >

    

def securityCam():
    cam = cv2.VideoCapture(1)
    while cam.isOpened():
        ret, frame1 = cam.read()
        ret, frame2 = cam.read()
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            if cv2.contourArea(c) < 5000:
                continue
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            winsound.Beep(800, 400)
        if cv2.waitKey(10) == ord('q'):
            break
        cv2.imshow('Security Camera', frame1)



def talk(text):
    engine.say(text)
    engine.runAndWait()


def send_email(receiver, subject, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    # Make sure to give app access in your Google account
    #For that go to gogle account then click on security option at the left 
    # then click on less secure app access at the bottom and turn on it.
    server.login('Enter your Email like ( koushik15-12971@diu.edu.bd )', 'Set password here')
    email = EmailMessage()
    email['From'] = 'koushik15-12971@diu.edu.bd'
    email['To'] = receiver
    email['Subject'] = subject
    email.set_content(message)
    server.send_message(email)


email_list = {
    #pronounciation must have clear
    
    'Aziz':'abdur15-12969@diu.edu.bd',
    'Imran': 'asadullah15-12981@diu.edu.bd',
    'Koushik':'koushik15-12971@diu.edu.bd',
    'Sajol': 'shahariar15-12981@diu.edu.bd'

}


def get_email_info():
    talk('To Whom you want to send email')
    name = takeCommand()
    receiver = email_list[name]
    print(receiver)
    talk('What is the subject of your email?')
    subject = takeCommand()
    talk('Tell me the text in your email')
    message = takeCommand()
    send_email(receiver, subject, message)
    talk('Sir. Your email is sent')
    talk('Do you want to send more email?')
    send_more = takeCommand()
    if 'yes' in send_more:
        get_email_info()
    



if __name__ == "__main__":
    wishMe()
    speak("I am Kirol. Please tell me how may I help you")
    while True:
    
        query = takeCommand().lower()
        
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=15)
            speak("According to Wikipedia")
            print(results)
            speak(results)
           
        # search option =========================================== >
        elif 'open google' in query:
            webbrowser.open("google.com")
            
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
            
        elif 'open stack overflow' in query:
            webbrowser.open("stackoverflow.com")

        elif 'open w3schools' in query:
            webbrowser.open("w3schools.com")
            
        elif 'open dashboard' in query:
            webbrowser.open("elearn.daffodilvarsity.edu.bd/?redirect=0")
        # search option =========================================== >

        # music player =========================================== >
        elif 'play music' in query:
            music_dir = 'C:\\Users\\Koushik\\Desktop\\DesktopAssistant_kirol\\music.mp3'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'security cam' in query:
            securityCam()

        elif 'send mail' in query:
            get_email_info()

        elif 'play' in query:
            song = query.replace('play', '')
            talk('playing ' + song)
            pywhatkit.playonyt(song)  

        else:
            speak('Sorry sir! I can not recognize it. If you say anything please tell me again.')


       