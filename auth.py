from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        nickname = request.form['nickname']
        password = generate_password_hash(request.form['password'])

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('User already exists!')
            return redirect(url_for('auth.register'))

        new_user = User(email=email, nickname=nickname, password_hash=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_or_nickname = request.form['email_or_nickname']
        password = request.form['password']
        user = User.query.filter((User.email == email_or_nickname) | (User.nickname == email_or_nickname)).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return redirect(url_for('jokes.leave_joke'))
        else:
            flash('Login failed. Check your credentials.')
    return render_template('login.html')