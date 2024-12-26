from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'  

db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all() 

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not full_name or not username or not email or not password:
            flash('Please fill in all fields.', 'error')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address already exists. Please use a different email.', 'error')
            return redirect(url_for('register'))

        new_user = User(full_name=full_name, username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('register'))

    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:  
            flash('Login successful!', 'success')
            session['user_id'] = user.id  
            return redirect(url_for('index'))  
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')

@app.route('/pg1')
def pg1():
    return render_template('pg1.html')

@app.route('/pg2')
def pg2():
    return render_template('pg2.html')

@app.route('/pg3')
def pg3():
    return render_template('pg3.html')

@app.route('/requese_password')
def requese_password():
    return render_template('requese_password.html')

@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)