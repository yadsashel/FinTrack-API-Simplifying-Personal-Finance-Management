# FinTrack API - Simplifying Personal Finance Management

## 🚀 Project Description

**FinTrack API** is a backend service designed to help manage personal finances effectively. It provides APIs for user registration, login, and managing financial tasks, such as tracking expenses, budgets, and savings. Built using **Python Flask** and **MongoDB**, this project ensures a smooth and secure database connection for handling user data.

---

## 🛠️ Features

- **User Management**: Register and authenticate users securely.
- **MongoDB Integration**: Store and retrieve user data with MongoDB.
- **Error Handling**: Robust error management for database and authentication processes.
- **Environment Variables**: Secure handling of sensitive information with `.env` files.

---

## 🗂️ Project Structure

```
FinTrack/
│
├── app.py                   # Main Flask application file
├── config.py                # Database connection setup using dotenv
├── .env                     # Environment variables file (MongoDB URI)
├── requirements.txt         # Project dependencies
├── .gitignore               # Ignore sensitive files and unnecessary directories
└── README.md                # Project documentation
```

---

## 💻 Setup Instructions

Follow these steps to set up and run the project locally:

### 1. **Clone the Repository**
```bash
git clone <repository_url>
cd FinTrack
```

### 2. **Set Up Environment Variables**
Create a `.env` file in the root directory and add the following:
```plaintext
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-url>/?retryWrites=true&w=majority&appName=Cluster0
```
Replace `<username>`, `<password>`, and `<cluster-url>` with your MongoDB credentials.

### 3. **Create a Virtual Environment**
```bash
python -m venv fintrack_env
source fintrack_env/bin/activate  # On Windows: fintrack_env\Scripts\activate
```

### 4. **Install Dependencies**
Install the required libraries using `pip`:
```bash
pip install -r requirements.txt
```

### 5. **Run the Application**
Start the Flask development server:
```bash
python app.py
```

The API will run locally on `http://127.0.0.1:5000`.

---

## 📦 Dependencies

- **Flask** - Python micro web framework
- **PyMongo** - MongoDB driver for Python
- **python-dotenv** - For environment variable management

Install all dependencies using:
```bash
pip install -r requirements.txt
```
---

## 📜 License

This project is licensed under the **MIT License**.

---

## 💬 Contact

For questions, suggestions, or issues, feel free to reach out:

- **Name**: [Your Name]
- **Email**: [Your Email]
- **GitHub**: [Your GitHub Username]

---

## 🌟 Acknowledgements

Special thanks to the tools and libraries that made this project possible:
- **MongoDB Atlas**
- **Python Flask**
- **PyMongo**

---

### 🚀 Future Enhancements
- Add user authentication with JWT tokens.
- Integrate frontend UI for user interaction.
- Implement financial reports and analytics.