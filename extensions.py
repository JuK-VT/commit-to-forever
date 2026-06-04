import json
import os

import firebase_admin
from firebase_admin import credentials, firestore

_db = None


def get_db():
    global _db
    if _db is None:
        _db = _connect()
    return _db


def _connect():
    if firebase_admin._apps:
        return firestore.client()

    cred_value = os.environ.get('FIREBASE_CREDENTIALS')
    if not cred_value:
        raise RuntimeError(
            'La variable de entorno FIREBASE_CREDENTIALS no está configurada.'
        )

    # Production: JSON string. Local: file path.
    if cred_value.strip().startswith('{'):
        cred = credentials.Certificate(json.loads(cred_value))
    else:
        cred = credentials.Certificate(cred_value)

    firebase_admin.initialize_app(cred)
    return firestore.client()
