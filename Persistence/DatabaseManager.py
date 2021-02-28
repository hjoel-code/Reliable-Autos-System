import firebase_admin
from firebase_admin import credentials, firestore, storage



import pyrebase

cred = credentials.Certificate('./javvy-autozone-firebase-adminsdk-ogsma-8b54558a09.json')
default_app = firebase_admin.initialize_app(cred)

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


class DatabaseManager:

    def __init__(self, collection):
        self.collection = firestore.client().collection(collection)
        self.querries = self.collection
        self.storage = firebase.storage()

    def write(self, docID, obj):

        response = {
            "status": False,
            "error": None
        }

        doc_ref = self.collection.document() if docID == "" else self.collection.document(docID)
        print('\nPlease wait...')
        try:
            doc_ref.set(obj.__dict__)
            response["status"] = True
            print("Successfully added to collection")
        except Exception as error:
            print(error)
            response["error"] = error
        return response 

    def read(self, docID):

        response = {
            "status": False,
            "error": None,
            "data": None
        }

        doc_ref = self.collection.document(docID)
        print('\nPlease wait...')
        try:
            response["data"] = doc_ref.get()
            response["status"] = True
            print("Successfully received object")
        
        except Exception as error:
            response["error"] = error
            print(error)

        
        return response

    def update(self, docID, obj):
        response = {
            "status": False,
            "error": None
        }

        doc_ref = self.collection.document(docID)
        print('\nPlease wait...')
        try:
            doc_ref.update(obj)
            response["status"] = True
        
        except Exception as error:
            response["error"] = error
            print(error) 

        return response

    def remove(self, docID):
        response = {
            "status": False,
            "error": None
        }

        doc_ref = self.collection.document(docID)
        print('\nPlease wait...')
        try:
            doc_ref.delete()
            response["status"] = True
            print("Successfully removed object")
       
        except Exception as error:
            response["error"] = error
            print(error)

        return response

    def getCollection(self):

        response = {
            "status": False,
            "error": None,
            "data": None
        }

        try:
            response["data"] = self.collection.get()
            response["status"] = True
        except Exception as error:
            response["error"] = error
        
        return response

    def addQuery(self, field, operator, value):
        response = {
            "status" : False,
            "error" : None
        }

        try:
            self.querries = self.querries.where(u""+field,u""+operator,value)
            response["status"] = True
        except Exception as error:
            response["error"] = error
        return response

    def resetQuery(self):
        self.querries = self.collection

    def getQuerriedDocs(self):
        response = {
            "status": False,
            "error": None,
            "data": None
        }

        print('\nPlease wait...')
        try:  
            response["data"] = self.querries.stream()
            response["status"] = True
        except Exception as error:
            response["error"] = error
        return response

    def storeFile(self, fileSource, fileDestination):
        img = self.storage.child(fileDestination).put(fileSource)
        return self.storage.child(fileDestination).get_url(img['downloadTokens'])





