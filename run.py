from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'your_secret_key'

# Настройка системы аутентификации
login_manager = LoginManager()
login_manager.init_app(app)

# Модели данных
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Gym:
    def __init__(self, id, name, latitude, longitude):
        self.id = id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

class SubscriptionOption:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

class Workout:
    def __init__(self, id, name, date, user_id):
        self.id = id
        self.name = name
        self.date = date
        self.user_id = user_id

# Имитация базы данных
users = {
    1: User(1, 'user1', 'password1'),
    2: User(2, 'user2', 'password2')
}

gyms = [
    Gym(1, 'Gym A', 40.730610, -73.935242),
    Gym(2, 'Gym B', 40.742057, -73.989481),
    Gym(3, 'Gym C', 40.752179, -73.971867)
]

subscription_options = [
    SubscriptionOption(1, 'Basic', 49.99),
    SubscriptionOption(2, 'Premium', 99.99),
    SubscriptionOption(3, 'Deluxe', 149.99)
]

workouts = [
    Workout(1, 'Strength Training', datetime(2023, 5, 1), 1),
    Workout(2, 'Cardio', datetime(2023, 5, 15), 1),
    Workout(3, 'Yoga', datetime(2023, 6, 1), 2)
]

# Маршруты
@app.route('/')
def index():
    return render_template('workouts.html', gyms=gyms, subscription_options=subscription_options, current_user=current_user)

@app.route('/workouts')
def workouts():
    return render_template('workouts.html', gyms=gyms, subscription_options=subscription_options, current_user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = next((user for user in users.values() if user.username == username), None)
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/subscription/checkout')
@login_required
def subscription_checkout():
    # Обработка покупки подписки
    return redirect(url_for('index'))

@app.route('/map')
def map():
    return render_template('map.html', gyms=gyms)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Обработка регистрации
        username = request.form['username']
        password = request.form['password']
        # Создание нового пользователя и добавление его в базу данных
        new_user = User(len(users) + 1, username, password)
        users[new_user.id] = new_user
        flash('You have been registered successfully. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@login_manager.user_loader
def load_user(user_id):
    return users.get(int(user_id))

if __name__ == '__main__':
    app.run(debug=True)
