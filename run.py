from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

users = {
    1: User(1, 'user1', 'password1'),
    2: User(2, 'user2', 'password2')
}

gyms = [
    {'id': 1, 'name': 'Gym A', 'latitude': 40.730610, 'longitude': -73.935242},
    {'id': 2, 'name': 'Gym B', 'latitude': 40.742057, 'longitude': -73.989481},
    {'id': 3, 'name': 'Gym C', 'latitude': 40.752179, 'longitude': -73.971867}
]

subscription_options = [
    {'id': 1, 'name': 'Basic', 'price': 49.99},
    {'id': 2, 'name': 'Premium', 'price': 99.99},
    {'id': 3, 'name': 'Deluxe', 'price': 149.99}
]

workouts = [
    {'id': 1, 'name': 'Strength Training', 'date': datetime(2023, 5, 1), 'user_id': 1},
    {'id': 2, 'name': 'Cardio', 'date': datetime(2023, 5, 15), 'user_id': 1},
    {'id': 3, 'name': 'Yoga', 'date': datetime(2023, 6, 1), 'user_id': 2}
]

@app.route('/gym/<int:gym_id>')
def gym_detail(gym_id):
    gym = next((g for g in gyms if g['id'] == gym_id), None)
    if gym:
        return render_template('gym_detail.html', gym=gym)
    else:
        return "Gym not found", 404

@app.route('/')
@app.route('/workouts')
def workouts():
    return render_template('workouts.html', gyms=gyms, subscription_options=subscription_options, current_user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = next((user for user in users.values() if user.username == username), None)
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('workouts'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('workouts'))

@app.route('/subscription/checkout')
@login_required
def subscription_checkout():
    # Обработка покупки подписки
    return redirect(url_for('workouts'))

@app.route('/map')
def map():
    return render_template('map.html', gyms=gyms)

if __name__ == '__main__':
    app.run(debug=True)
