import firebase_admin
from firebase_admin import credentials, storage
import os

from dotenv import load_dotenv
# from data import firebase_bucket_url
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(BASE_DIR, 'firebase_cred.json')

# initialize the Firebase Admin SDK
cred = credentials.Certificate(cred_path)
# initialize the Firebase Admin SDK
firebase_admin.initialize_app(cred, {
    'storageBucket': os.getenv('FIREBASE_BUCKET_URL')
})

# get the Firebase Storage bucket
bucket = storage.bucket()
