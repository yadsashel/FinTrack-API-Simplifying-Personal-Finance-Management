import os
import sys
from flask import Flask, sessions, render_template, signals, redirect, url_for, Response, flash, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo.mongo_client import MongoClient #remember in here you imported that for fixing the problem of database error
from pymongo.server_api import ServerApi #also this
from dotenv import load_dotenv
import bcrypt
from bson import ObjectId 
from flask_cors import CORS 

#creating the flask app
app = Flask(__name__)
CORS(app)

#seeting up a secret key for securing session
app.secret_key = '#Fp23@/3mOk'

# Load environment variables from .env
load_dotenv()

#connect to the database
#remember that you can find that code in the mongo db (connect) for another project to use it eaaasly bro 
# Fetch the MongoDB URI from .env
uri = os.getenv("MONGODB_URI")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

#Access the 'fintrack_db' database
db = client["fintrack_db"]

# Access the 'users' collection within 'fintrack_db'
users_collection = db["users"]

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

#route for the home page
@app.route('/')
def index():
    return render_template('index.html')

#route for the dashboard 
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

#route for add transaction 
@app.route('/addtransaction')
def addtransaction():
    return render_template('addtransaction.html')

#route for view transaction
@app.route('/viewtransaction')
def viewtransaction():
    return render_template('viewtransaction.html')

#route for profile
@app.route('/profile')
def profile():
    return render_template('profile.html')

#route for analytics page
@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

#route for seetings page
@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validate inputs
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('register'))

        # Hash password and save user
        hashed_password = generate_password_hash(password)
        try:
            new_user = {
                'full_name': full_name,
                'email': email,
                'password': hashed_password
            }
            users_collection.insert_one(new_user)
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Database error: {str(e)}', 'error')
            return redirect(url_for('register'))

    return render_template('register.html')

#route for login 
@app.route('/login')
def login():
    return render_template('login.html')

#route for logout 
@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/forgotpassword')
def forgotpassword():
    return render_template('forgotpassword.html')

if __name__ == '__main__':
    app.run(debug=True) 