☔ Automated Weather Reminder App

An automated weather reminder web app that alerts users via SMS if it’s going to rain in their area — so they never forget their umbrella! 🌧️ Built using Python for the backend logic, integrated with Flask, HTML/CSS, SQLAlchemy, Twilio, and Google Weather API.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

🚀 Features

🧑‍💼 User Registration & Login
Users can securely create an account, log in, and log out.

🔐 Password Hashing & Authentication
User credentials are protected using hashed passwords and stored in an SQLite database via SQLAlchemy ORM.

📍 Location Input
Users submit their location through a responsive HTML/CSS frontend.

🌦️ Automated Daily Rain Check
A Python script runs daily to fetch weather data for each user's location using the Google Weather API.

📲 SMS Notifications via Twilio
If rain is expected, users receive an SMS alert through Twilio.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
🧰 Tech Stack

Backend Logic: Python

Web Framework: Flask

Frontend: HTML & CSS

Database: SQLite (with SQLAlchemy ORM)

APIs: Google Weather API, Twilio

Auth: Password hashing (e.g., werkzeug.security)
