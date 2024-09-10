import firebase_admin
from firebase_admin import credentials, storage
import os
import json

from dotenv import load_dotenv
# from data import firebase_bucket_url
load_dotenv()

cred_dict = json.loads(os.getenv('FIREBASE_CREDENTIALS_JSON'))
# initialize the Firebase Admin SDK
cred = credentials.Certificate(cred_dict)
# initialize the Firebase Admin SDK
firebase_admin.initialize_app(cred, {
    'storageBucket': os.getenv('FIREBASE_BUCKET_URL')
})

# get the Firebase Storage bucket
bucket = storage.bucket()
