import streamlit as st
import bcrypt
import jwt
import datetime
import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Secret key for JWT
JWT_SECRET = os.getenv("JWT_SECRET", "your_secret_key")
JWT_EXPIRY_HOURS = int(os.getenv("JWT_EXPIRY_HOURS", 1))

# Function to securely hash a password
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Function to verify a password
def check_password(plain_text, hashed_password):
    return bcrypt.checkpw(plain_text.encode(), hashed_password.encode())

# Function to create a JWT token
def create_jwt_token(username, role):
    payload = {
        "username": username,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=JWT_EXPIRY_HOURS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

# Function to decode JWT token
def decode_jwt_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        st.error("Session expired. Please log in again.")
        return None
    except jwt.InvalidTokenError:
        st.error("Invalid token. Please log in again.")
        return None
