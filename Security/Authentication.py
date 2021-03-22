from Persistence.DatabaseManager import DatabaseManager
import pyrebase
import urllib.request
from urllib.error import HTTPError

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

class User:

    def __init__(self, fname = '', lname = '', uid = ''):
        self.fname = fname
        self.lname = lname
        self.uid = uid

    def getDisplayName(self):
        return self.fname + ' ' + self.lname

    def toObject(self, doc):
        self.fname = doc['fname']
        self.lname = doc['lname']
        self.uid = doc['uid']


class Authentication:
    def __init__(self):
        self.auth = firebase.auth()
        self.db = DatabaseManager('Users')
        self.user = None
        self.isUser = False

    def signIn(self, email, password):
        response = {
            'status': False,
            'error': None
        }
        
        try:
            user = self.auth.sign_in_with_email_and_password(email, password)
            response = self.db.read(user['localId'])
            if (response['status']):
                self.user = User()
                self.user.toObject(response['data'].to_dict())
                self.isUser = True

        except Exception as error:
            print('Authentication Fail')
            response['error'] = error
        
        return response


    def signUpUser(self, firstName, lastName, email_new, password_new):
        response = {
            'status': False,
            'error': None
        }
        try:
            user = self.auth.create_user_with_email_and_password(email_new, password_new)
            data = User(firstName, lastName, user['localId'])
            response = self.db.write(user['localId'], data)
        except Exception as error:
            response['status'] = False
            response['error'] = error
        
        return response

    def signOut(self):
        self.user = None
        self.isUser = False


