from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy import Integer,String
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os


app = Flask(__name__)
load_dotenv(dotenv_path='env')
app.secret_key = os.getenv('app_secret_key')

#--------------------------------------------- Creating Database -------------------------------------------------------
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///weather_user_account.db'
db.init_app(app)

class Account(db.Model):
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    name: Mapped[str] = mapped_column(String(250),nullable=False)
    email: Mapped[str] = mapped_column(String(8),unique=True,nullable=False)
    password: Mapped[str] = mapped_column(String(250),nullable=False)
    location: Mapped[str] = mapped_column(String(250),nullable=True)
    phone_number: Mapped[str] = mapped_column(String(10),nullable=False)

with app.app_context():
    db.create_all()

#----------------------------------------------------------------------------------------------------------------------

@app.route('/',methods=['GET','POST'])
def login_page():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        print(f'Login attempt email = {email}, password = {password}')

        #1. Retrieve hashed password based on phone_number.
        #2. Compare hashed password with password user keyed in

        hashed_password = db.session.execute(db.select(Account.password).where(Account.email == email)).scalar()

        if not(check_password_hash(pwhash=hashed_password,password=password)):
            return "Invalid credentials", 400

        current_user_id = db.session.execute(db.select(Account.id).where(Account.email == email)).scalar()
        session['current_user'] = current_user_id

        print(session['current_user'])

        return redirect(url_for('weather_page'))
    return render_template('login.html')

#

@app.route('/register',methods=['GET','POST'])
def register_page():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone_number = request.form['phone_number']
        phone_number = '+65' + phone_number

        if not email or not password or not phone_number:
            return 'All fields are required',400

        #Check if email and phone number already taken.

        email_not_available = db.session.execute(db.select(Account.email).where(Account.email == email)).scalar()
        phone_not_available = db.session.execute(db.select(Account.phone_number).where(Account.phone_number == phone_number)).scalar()
        if email_not_available or phone_not_available:
            return 'User already have an account',400
        else:
            #Hasing of password
            hashed_password = generate_password_hash(password)
            #create new record in database
            new_user = Account(name=name,email=email,password=hashed_password,phone_number=phone_number)
            db.session.add(new_user)
            db.session.commit()

        return redirect(url_for('login_page'))
    return render_template('register.html')

@app.route('/weather',methods=['GET','POST'])
def weather_page():
    if 'current_user' not in session:
        return redirect(url_for('login_page'))
    if request.method == 'POST':
        location = request.form['location']
        location_to_update = db.session.execute(db.select(Account).where(Account.id == session['current_user'])).scalar()
        location_to_update.location = location
        db.session.commit()
        return redirect(url_for('success_page'))
    return render_template('weather.html')


@app.route('/success')
def success_page():
    return render_template('success.html')


if __name__ == '__main__':
    app.run(debug=True)