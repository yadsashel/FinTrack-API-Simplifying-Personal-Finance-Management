import os
import sys
from flask import Flask, session, render_template, signals, redirect, url_for, Response, flash, jsonify, request, json
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo.mongo_client import MongoClient #remember in here you imported that for fixing the problem of database error
from pymongo.server_api import ServerApi #also this
from dotenv import load_dotenv
from flask_pymongo import PyMongo
import bcrypt
from bson.objectid import ObjectId  # For working with MongoDB ObjectId
from flask_cors import CORS 
from datetime import datetime, timedelta
from functools import wraps

#creating the flask app
app = Flask(__name__)
CORS(app)

app.secret_key = '#Fp23@/3jmOk' #seeting up a secret key for securing session

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
transactions_collection = db["transaction"]

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

#route for add transaction 
@app.route('/addtransaction', methods=['GET', 'POST'])
def addtransaction():
    if request.method == 'POST':
        try:
            # Ensure the user_id is in the session
            user_id = session.get('user_id')
            if not user_id:
                flash('Error: User not logged in', 'error')
                return redirect('/login')  # Redirect to login if not logged in

            # Convert user_id from string to ObjectId
            user_id = ObjectId(user_id)

            # Extract data from the form
            date = datetime.strptime(request.form['transaction-date'], '%Y-%m-%d')
            type_ = request.form['transaction-type']
            category = request.form['transaction-category']
            amount = float(request.form['transaction-amount'])

            # Insert transaction into MongoDB
            transaction = {
                "date": date,
                "type": type_,
                "category": category,
                "amount": amount,
                "user_id": user_id  # Store user_id as ObjectId
            }
            transactions_collection.insert_one(transaction)

            flash('Transaction added successfully!', 'success')
            return redirect('/addtransaction')

        except Exception as e:
            flash(f'An error occurred: {e}', 'error')
            return redirect('/addtransaction')

    return render_template('addtransaction.html')


# Route for view transaction page
@app.route('/viewtransaction', methods=['GET', 'POST'])
def viewtransaction():
    try:
        if request.method == 'POST':
            action = request.json.get('action')
            transaction_id = request.json.get('id')

            if not transaction_id or not action:
                return jsonify({"message": "Missing action or transaction ID"}), 400

        # GET request: Fetch transactions
        transactions = list(transactions_collection.find())
        for transaction in transactions:
            transaction["_id"] = str(transaction["_id"])  # Convert ObjectId to string for JSON serialization
            if "date" in transaction:
                if isinstance(transaction["date"], str):
                    try:
                        transaction["date"] = datetime.strptime(transaction["date"], "%Y-%m-%d")
                    except ValueError:
                        transaction["date"] = None  # Handle invalid dates gracefully
                elif not isinstance(transaction["date"], datetime):
                    transaction["date"] = None

        return render_template('viewtransaction.html', transactions=transactions)

    except Exception as e:
        flash(f"Error loading transactions: {str(e)}", "error")
        return redirect(url_for('home'))


#delete a transaction
@app.route('/delete-transaction/<transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    try:
        transactions_collection.delete_one({"_id": ObjectId(transaction_id)})
        return jsonify({"success": True, "message": "Transaction deleted successfully."}), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Error deleting transaction: {str(e)}"}), 500



# Route for profile
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    # Check if the user is logged in
    if 'user_id' not in session:
        flash('Please log in to access your profile', 'error')
        return redirect(url_for('login'))
    
    try:
        user_id = ObjectId(session['user_id'])  # Convert string to ObjectId
    except Exception:
        flash('Invalid user ID', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Get form data
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        address = request.form.get('address')
        phone = request.form.get('phone')
        
        # Validate password match
        if password and password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('profile'))

        # Prepare update data (exclude empty fields)
        update_data = {}
        if full_name: update_data['full_name'] = full_name
        if email: update_data['email'] = email
        if address: update_data['address'] = address
        if phone: update_data['phone'] = phone
        if password: 
            update_data['password'] = generate_password_hash(password)

        # Update the user in the database
        try:
            result = users_collection.update_one({'_id': user_id}, {'$set': update_data})
            if result.matched_count == 0:
                flash('User not found during update', 'error')
            else:
                flash('Profile updated successfully', 'success')
        except Exception:
            flash('An error occurred while updating your profile', 'error')

        return redirect(url_for('profile'))

    # For GET requests, fetch user data
    try:
        user = users_collection.find_one({'_id': user_id})
        if not user:
            flash('User not found', 'error')
            return redirect(url_for('login'))
    except Exception:
        flash('An error occurred while fetching your profile', 'error')
        return redirect(url_for('login'))

    # Render the profile page with user data
    return render_template('profile.html', user=user)

#route for analytics page
@app.route('/analytics', methods=['GET'])
def analytics():
    try:
        # Fetch all transactions
        transactions = list(transactions_collection.find({}))

        # Ensure all transaction dates are datetime objects
        for t in transactions:
            if isinstance(t.get("date"), str):  # Convert string dates to datetime
                try:
                    t["date"] = datetime.strptime(t["date"], "%Y-%m-%d")
                except ValueError:
                    t["date"] = None  # Handle invalid date formats gracefully

        # Filter out transactions with invalid or missing dates
        transactions = [t for t in transactions if t["date"] is not None]

        # Calculate totals
        total_income = sum(float(t.get("amount", 0)) for t in transactions if t.get("type") == "income")
        total_expenses = sum(float(t.get("amount", 0)) for t in transactions if t.get("type") == "expense")
        savings = total_income - total_expenses

        # Group expenses by category
        expenses_by_category = {}
        for t in transactions:
            if t.get("type") == "expense":
                category = t.get("category", "Uncategorized")
                expenses_by_category[category] = expenses_by_category.get(category, 0) + float(t.get("amount", 0))

        # Prepare data for spending trends (group by date)
        spending_trends = {}
        for t in transactions:
            if t.get("date"):
                date_str = t["date"].strftime("%Y-%m-%d")  # Convert datetime to string for grouping
                amount = float(t.get("amount", 0))
                spending_trends[date_str] = spending_trends.get(date_str, 0) + amount

        # Sort spending trends by date
        spending_trends = sorted(spending_trends.items())  # Returns a list of (date, amount) tuples

        # Convert data for Chart.js
        category_labels = list(expenses_by_category.keys())
        category_values = list(expenses_by_category.values())
        trend_dates = [date for date, _ in spending_trends]
        trend_amounts = [amount for _, amount in spending_trends]

        # Pass data to the analytics HTML template
        return render_template(
            'analytics.html',
            total_income=total_income,
            total_expenses=total_expenses,
            savings=savings,
            category_labels=json.dumps(category_labels),
            category_values=json.dumps(category_values),
            trend_dates=json.dumps(trend_dates),
            trend_amounts=json.dumps(trend_amounts)
        )
    except Exception as e:
        # Handle unexpected errors gracefully
        flash(f"Error loading analytics data: {str(e)}", "error")
        return redirect(url_for('home'))  # Redirect to a safe page if an error occurs
    
#Add the New Filtering Route
@app.route('/filter-user-data', methods=['GET'])
def filter_user_data():
    try:
        # Get the logged-in user's ID from the session
        user_id = session.get('user_id')  # User ID stored as string

        if not user_id:
            return jsonify({"success": False, "message": "Unauthorized access"}), 401

        # Debugging: Print the user_id for verification
        print(f"Filtering data for user_id: {user_id}")

        # Fetch data for the logged-in user only
        transactions = list(transactions_collection.find())

        # Debugging: Log fetched transactions
        print(f"Fetched Transactions: {transactions}")

        # Format transactions for JSON response
        for transaction in transactions:
            transaction["_id"] = str(transaction["_id"])  # Convert ObjectId to string
            if "date" in transaction and isinstance(transaction["date"], datetime):
                transaction["date"] = transaction["date"].strftime("%Y-%m-%d")

        return jsonify({"success": True, "data": transactions}), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500



#route for register page
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
        
        #check if the email is alreeady exist
        if users_collection.find_one({'email': email}):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
            flash('this email is already exist, please try this email.', 'error')
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
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("POST request received")  # Debugging log

        # Get form data
        email = request.form.get('email')
        password = request.form.get('password')

        # Debugging logs for received data
        print(f"Email: {email}, Password: {password}")
    
        # Check if email and password are provided
        if not email or not password:
            flash('Please provide both email and password', 'error')
            return redirect(url_for('login'))

        # Check if the user exists in the db
        user = users_collection.find_one({'email': email})
        print(f"User from DB: {user}")

        if not user:
            flash('User not found, please register first.', 'error')
            return redirect(url_for('login'))

        # Validate password 
        if not check_password_hash(user['password'], password):
            flash('Password is incorrect, try again.', 'error')
            return redirect(url_for('login'))

        # Save user details in session
        session['user_id'] = str(user['_id'])  # Store user ID
        session['email'] = user['email']  # Store email

        # Flash success message
        flash('Login successful', 'success')

        # Redirect to profile page
        return redirect(url_for('profile'))  # Use redirect to ensure navigation

    print("GET request received")  # Debugging log

    # If it's a GET request, render the login page
    return render_template('login.html')

#route for logout 
@app.route('/logout')
def logout():
    session.clear()  # Clear all session data
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

#route for forgort password page
@app.route('/forgotpassword')
def forgotpassword():
    return render_template('forgotpassword.html')

#route for privacy and policy page
@app.route('/privacy')
def privacy_page():
    return render_template('privacy.html')


#route for terms and condition
@app.route('/terms')
def terms():
    return render_template('terms.html')

#route for terms and condition
@app.route('/fqa')
def fqa():
    return render_template('fqa.html')
   


if __name__ == '__main__':
    app.run(debug=True) 