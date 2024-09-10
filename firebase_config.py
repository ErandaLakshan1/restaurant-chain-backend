import firebase_admin
from firebase_admin import credentials, storage
import os
import json

from dotenv import load_dotenv
# from data import firebase_bucket_url
load_dotenv()

firebase_cred_json = os.getenv('FIREBASE_CREDENTIALS_JSON')

if not firebase_cred_json:
    raise ValueError("FIREBASE_CREDENTIALS_JSON environment variable is not set.")

try:
    cred_dict = json.loads(firebase_cred_json)
except json.JSONDecodeError as e:
    raise ValueError(f"Error decoding JSON from FIREBASE_CREDENTIALS_JSON: {e}")
# initialize the Firebase Admin SDK
cred = credentials.Certificate(cred_dict)
# initialize the Firebase Admin SDK
firebase_admin.initialize_app(cred, {
    'storageBucket': os.getenv('FIREBASE_BUCKET_URL')
})

# get the Firebase Storage bucket
bucket = storage.bucket()
