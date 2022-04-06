# Todo Taking responce from onwer and tell to visitor --- done
# Face recog accuracy increase
# Visitor comming time
# Save visitor data with time

from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pydoc import plain
import face_recognition
import cv2
import pyttsx3
import datetime
from playsound import playsound
import smtplib
import imghdr
import os
import time
from time import sleep
import numpy as np
from sendgrid.helpers.mail import Mail, Email, To, Content
import email.mime
import keyboard
from pynput.keyboard import Key, Listener
import keyboard
import speech_recognition as sr
from email.message import EmailMessage
import pyrebase

def speech_to_text():
    r = sr.Recognizer()

    def SpeakText(command):
        engine = pyttsx3.init()
        engine.say(command)
        engine.runAndWait()

    while(1):
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
                audio2 = r.listen(source2)
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()
#                 print("Did you say "+MyText)
                return MyText
        except sr.RequestError as e:
            #             print("Could not request results; {0}".format(e))
            MyText = 'No response'
            return MyText
        except sr.UnknownValueError:
            #             print("unknown error occured")
            MyText = 'No response'
            return MyText

def greeting():
    curr_time = datetime.datetime.now()
    curr_time = str(curr_time.hour).zfill(2)+str(curr_time.minute).zfill(2)
    if(curr_time > '0000' and curr_time <= '1159'):
        engine = pyttsx3.init()
        engine.say("good morning")
        engine.runAndWait()
    elif(curr_time <= '1700'):
        engine = pyttsx3.init()
        engine.say("good afternoon")
        engine.runAndWait()
    else:
        engine = pyttsx3.init()
        engine.say("good evening")
        engine.runAndWait()

def capture_image():
    videoCaptureObject = cv2.VideoCapture(0)
    result = True
    while(result):
        ret, frame = videoCaptureObject.read()
        cv2.imwrite("visitor.jpg", frame)
        result = False
    videoCaptureObject.release()
    cv2.destroyAllWindows()

def update_to_null():
    firebaseConfig={
    "apiKey": "AIzaSyAQ2FU-OaJzklkEafaWYyMV6kwRzWf-_jU",
    "authDomain": "sem4project-95dfc.firebaseapp.com",
    "databaseURL": "https://sem4project-95dfc-default-rtdb.firebaseio.com",
    "storageBucket": "sem4project-95dfc.appspot.com",
    "projectId": "sem4project-95dfc",
    "messagingSenderId": "1022736212561",
    "appId": "1:1022736212561:web:963267d1f68daa1501ce70",
    "measurementId": "G-Y89N81WJR6"
    }

    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()
    db.child("permission").update({"unlock":"null"})

def takeresponse():
    
    firebaseConfig={
        "apiKey": "AIzaSyAQ2FU-OaJzklkEafaWYyMV6kwRzWf-_jU",
        "authDomain": "sem4project-95dfc.firebaseapp.com",
        "databaseURL": "https://sem4project-95dfc-default-rtdb.firebaseio.com",
        "storageBucket": "sem4project-95dfc.appspot.com",
        "projectId": "sem4project-95dfc",
        "messagingSenderId": "1022736212561",
        "appId": "1:1022736212561:web:963267d1f68daa1501ce70",
        "measurementId": "G-Y89N81WJR6"
    }
    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()
    value = db.child("permission").child("unlock").get()
    print(value.val())
    return value.val()

def email(msg, ph):
    Sender_Email = "semesterfourproject@gmail.com"
    Reciever_Email = "semesterfourproject@gmail.com"
    Password = 'dokszeferkszivyv'

    newMessage = EmailMessage()                         
    newMessage['Subject'] = "Intruder alert!" 
    newMessage['From'] = Sender_Email                   
    newMessage['To'] = Reciever_Email     
    
    newMessage.set_content('Do you want to let him in?\nReason: ' + msg + '\nPhone number : ' + ph + 
                           "\nPlease give your response\n https://amanchaturvedi24.github.io/doorunlock/")
    with open('visitor.jpg', 'rb') as f:
        image_data = f.read()
        image_type = imghdr.what(f.name)
        image_name = f.name

    newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

        smtp.login(Sender_Email, Password)              
        smtp.send_message(newMessage)

def findEncodings(images):
    encodeList = []
    for i in images:
        i = cv2.cvtColor(i, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(i)[0]
        encodeList.append(encode)
    return encodeList

path = 'TestImages'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for i in myList:
    curImg = cv2.imread(f'{path}/{i}')
    images.append(curImg)
    classNames.append(os.path.splitext(i)[0])
print(classNames)
encodeListKnown = findEncodings(images)
print('Encoding Complete')

def recog():
    capture_image()

    cur = cv2.imread('visitor.jpg')
    imgSmall = cv2.resize(cur, (0, 0), None, 0.25, 0.25)
    imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgSmall)
    encodesCurFrame = face_recognition.face_encodings(imgSmall, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):

        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            engine = pyttsx3.init()
            engine.say("welcome")
            engine.say("door unlocked")
            engine.runAndWait()
            return name

        else:
            name = 'Unknown'
            
            engine = pyttsx3.init()
            engine.say("unknown visitor asking for permission")
            engine.say("please tell the reason for visiting")
            engine.runAndWait()
            msg = speech_to_text()
            print(msg)
            engine = pyttsx3.init()
            engine.say("please enter phone number through keyboard")
            engine.runAndWait()
            ph = input("Enter phone number : ")
            email(msg, ph)
            
            t_end = time.time() + 60
            flag = False
            
            while time.time() < t_end:
                response = takeresponse() 
                
                if(response=="yes"):
                    engine = pyttsx3.init()
                    engine.say("Welcome")
                    engine.runAndWait()
                    update_to_null()
                    flag = True
                    break

                if(response=="no"):
                    engine = pyttsx3.init()
                    engine.say("Sorry you can't enter")
                    engine.runAndWait()
                    update_to_null()
                    flag = True
                    break
                    
            if(flag==False):
                engine = pyttsx3.init()
                engine.say("Sorry you can come later as onwer is busy now")
                engine.runAndWait()
                from datetime import datetime
                now = datetime.now()
                cur = cv2.imread('visitor.jpg')
                cv2.imwrite('D:/Users/aman/OneDrive/Desktop/op/Security_System_for_Home/door_lock/Unattended/x.jpg', cur)
                image_time = now.strftime("%m-%d-%Y__%H-%M-%S") + '.jpg'
                image_name = "D:/Users/aman/OneDrive/Desktop/op/Security_System_for_Home/door_lock/Unattended/" + image_time
                os.rename("D:/Users/aman/OneDrive/Desktop/op/Security_System_for_Home/door_lock/Unattended/x.jpg", image_name)
                
        return name

while True:
    keyboard.wait("e")
    greeting()
    name = recog()
    print(name)
