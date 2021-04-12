import firebase_admin
from firebase_admin import credentials, firestore, storage
import pyrebase
from flask import Flask



# Firebase Admin Configuration
cred = credentials.Certificate('./Reliable-Autos-System/reliable-autos-firebase-adminsdk-ogsma-8b54558a09.json')
default_app = firebase_admin.initialize_app(cred)



# Pyrebase Configuration
config = {
    "apiKey": "AIzaSyBrZVMANrVDDLuqYJktyTDolrDsSDNyZHc",
    "authDomain": "javvy-autozone.firebaseapp.com",
    "databaseURL": "https://javvy-autozone.firebaseio.com",
    "projectId": "javvy-autozone",
    "storageBucket": "javvy-autozone.appspot.com",
    "messagingSenderId": "856400598410",
    "appId": "1:856400598410:web:05da134896fd41c386a473",
    "measurementId": "G-BGF0C71YEL"
  }

firebase = pyrebase.initialize_app(config)


# Flask Configuration
app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY=b"RELIABLE000SYS0012"
)