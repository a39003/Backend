from firebase_admin import firestore, storage, auth
import pyrebase

config = {
    "apiKey": "AIzaSyAOlYqfB9mIuKg0NR5agNaJ5LOTSNeUxEE",
    "authDomain": "inventorymanagements.firebaseapp.com",
    "projectId": "inventorymanagements",
    "storageBucket": "inventorymanagements.appspot.com",
    "messagingSenderId": "459842877639",
    "appId": "1:459842877639:web:eb3a8220aa9cff7744e6e2",
    "databaseURL": "https://console.firebase.google.com/u/3/project/inventorymanagements/database/inventorymanagements-"
                   "default-rtdb/data/~2F"
}
db = firestore.client()
firebase = pyrebase.initialize_app(config)
pyre_auth = firebase.auth()
