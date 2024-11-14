from flask import Blueprint, render_template, request, session, redirect, url_for
from models import Joke, User, db

jokes_bp = Blueprint('jokes', __name__)

@jokes_bp.route('/leave_joke', methods=['GET', 'POST'])
def leave_joke():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        user_id = session['user_id']
        
        new_joke = Joke(title=title, body=body, author_id=user_id)
        db.session.add(new_joke)
        
        user = User.query.get(user_id)
        user.joke_balance += 1
        
        db.session.commit()
        
        return redirect(url_for('jokes.my_jokes'))
    
    return render_template('leave_joke.html')

@jokes_bp.route('/my_jokes')
def my_jokes():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    jokes = Joke.query.filter_by(author_id=user_id).all()
    
    return render_template('my_jokes.html', jokes=jokes)

@jokes_bp.route('/view_joke/<int:joke_id>')
def view_joke(joke_id):
    joke = Joke.query.get(joke_id)
    
    if not joke:
        return redirect(url_for('jokes.my_jokes'))
    
    return render_template('view_joke.html', joke=joke)