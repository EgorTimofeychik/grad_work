from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    subscriptions = db.relationship('Subscription', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __str__(self):
        return f'<User {self.username}>'

    def __repr__(self):
        return f'<User {self.username}>'

class Gym(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    subscriptions = db.relationship('Subscription', backref='gym', lazy='dynamic')

    def __str__(self):
        return f'<Gym {self.name}>'

    def __repr__(self):
        return f'<Gym {self.name}>'

class SubscriptionType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    subscriptions = db.relationship('Subscription', backref='subscription_type', lazy='dynamic')

    def __str__(self):
        return f'<SubscriptionType {self.name}>'

    def __repr__(self):
        return f'<SubscriptionType {self.name}>'

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    gym_id = db.Column(db.Integer, db.ForeignKey('gym.id'), nullable=False)
    subscription_type_id = db.Column(db.Integer, db.ForeignKey('subscription_type.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    def __str__(self):
        return f'<Subscription {self.id}>'

    def __repr__(self):
        return f'<Subscription {self.id}>'

class WorkoutType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    workouts = db.relationship('Workout', backref='workout_type', lazy='dynamic')

    def __str__(self):
        return f'<WorkoutType {self.name}>'

    def __repr__(self):
        return f'<WorkoutType {self.name}>'

class Trainer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    hourly_rate = db.Column(db.Float, nullable=False)
    workouts = db.relationship('Workout', backref='trainer', lazy='dynamic')

    def __str__(self):
        return f'<Trainer {self.name}>'

    def __repr__(self):
        return f'<Trainer {self.name}>'

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    workout_type_id = db.Column(db.Integer, db.ForeignKey('workout_type.id'), nullable=False)
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainer.id'), nullable=True)
    start_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return f'<Workout {self.id}>'
    
    
    def __repr__(self):
        return f'<Workout {self.id}>'

