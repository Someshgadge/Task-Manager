import secrets
from flask import Flask

def generate_secret_key():
    return secrets.token_urlsafe(32)

app = Flask(__name__)
app.secret_key = generate_secret_key()

print("Generated secret key:", app.secret_key)
