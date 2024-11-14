from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jokes.db'

    db.init_app(app)

    # Import blueprints here to avoid circular imports
    from auth import auth_bp
    from jokes import jokes_bp

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(jokes_bp)

    @app.route('/')
    def index():
        return "Welcome to Master of Jokes!"

    return app

if __name__ == '__main__':
    app = create_app()
    
    # Create all tables if they don't exist
    with app.app_context():
        db.create_all()  # This creates all tables in your database
    
    app.run(debug=True)