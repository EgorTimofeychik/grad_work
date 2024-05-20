from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/dbname'
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    subscriptions = db.relationship('Subscription', secondary='user_subscription', backref=db.backref('users', lazy='dynamic'), lazy='dynamic')

user_subscription = db.Table('user_subscription',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('subscription_id', db.Integer, db.ForeignKey('subscription.id'))
)

class Gym(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    subscription_options = db.relationship('Subscription', backref='gym', lazy=True)

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    gym_id = db.Column(db.Integer, db.ForeignKey('gym.id'), nullable=False)

@app.route('/')
def index():
    return render_template('index.html', gyms=Gym.query.all())

@app.route('/login', methods=['GET', 'POST'])
def login():
    # login logic here
    pass

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # signup logic here
    pass

@app.route('/gym/<int:gym_id>')
@login_required
def gym(gym_id):
    gym = Gym.query.get_or_404(gym_id)
    return render_template('gym.html', gym=gym, subscriptions=gym.subscription_options)

@app.route('/buy/<int:subscription_id>')
@login_required
def buy(subscription_id):
    subscription = Subscription.query.get_or_404(subscription_id)
    if current_user.subscriptions.filter_by(id=subscription_id).first():
        flash('You already have this subscription')
        return redirect(url_for('gym', gym_id=subscription.gym_id))
    else:
        current_user.subscriptions.append(subscription)
        db.session.commit()
        flash('Subscription purchased successfully')
        return redirect(url_for('gym', gym_id=subscription.gym_id))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/map')
def gym_map():
    gyms = Gym.query.all()
    return render_template('map.html', gyms=gyms)

@app.route('/workouts')
def workouts():
    workouts = Workout.query.all()
    trainers = Trainer.query.all()
    return render_template('workouts.html', workouts=workouts, trainers=trainers)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255), nullable=False)

class Trainer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    bio = db.Column(db.String(255), nullable=False)
    workouts = db.relationship('Workout', backref='trainer', lazy=True)

if __name__ == '__main__':
    app.run(debug=True)