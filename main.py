from flask import Flask, render_template,request, redirect, url_for,send_from_directory
from flask_mail import Mail, Message
import json
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import os
import qrcode
from PIL import Image



with open("/Users/mananmehra/Desktop/YANAGRHA/config.json", "r") as c:
    params = json.load(c)["params"]
    
local_server=True 

app = Flask(__name__)

if local_server:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['local_uri']
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['prod_uri']
    
db = SQLAlchemy(app)

qrcodes_dir = os.path.join(app.root_path, 'static', 'qrcodes')
os.makedirs(qrcodes_dir, exist_ok=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50),unique=True,nullable=False)
    password=db.Column(db.String(50), nullable=False)
    confirm_password=db.Column(db.String(50), nullable=False)

class test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search_parking')
def search_parking():
    return render_template('search.html')

@app.route('/explore1')
def explore1():
    return render_template('explore1.html')

@app.route('/explore2')
def explore2():
    return render_template('explore2.html')

@app.route('/owner_registration')
def owner_registration():
    return render_template('owner_registration.html')

@app.route('/booking_confirmation')
def booking_confirmation():
    return render_template('booking_confirmation.html')

@app.route('/no_booking')
def no_booking():
    return render_template('no_booking.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('signup.html', error='Username already exists')

        # Check if password and confirm_password match
        if password != confirm_password:
            return render_template('signup.html', error='Passwords do not match')

        # Create a new user
        new_user = User(username=username, password=password,confirm_password=confirm_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            # Login successful, you might want to set a session variable or use a login manager
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')

    new_user = test(name=name, email=email, phone=phone)
    db.session.add(new_user)
    db.session.commit()

    # Generate QR code and save it
    generate_qr_code(name, phone)

    return redirect(url_for('success', name=name, phone=phone))

@app.route('/success')
def success():
    name = request.args.get('name')
    phone = request.args.get('phone')
    return render_template('success.html', name=name, phone=phone)

@app.route('/qrcodes/<filename>')
def qrcodes(filename):
    return send_from_directory('static/qrcodes', filename)

def generate_qr_code(name, phone):
    data_to_encode = f"Name: {name}\nPhone: {phone}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data_to_encode)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(os.path.join(qrcodes_dir, f'{name}_{phone}.png'))

if __name__ == '__main__':
    app.run(debug=True)
