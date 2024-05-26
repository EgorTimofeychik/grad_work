from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Gym, SubscriptionType, Trainer, WorkoutType
from config import Config

# Создание экземпляра Flask
app = Flask(__name__)
app.config.from_object(Config)

# Инициализация базы данных SQLAlchemy
db.init_app(app)
with app.app_context():
    db.create_all()

# Создание и инициализация менеджера авторизации
login_manager = LoginManager()
login_manager.init_app(app)

# Загрузчик пользователя для менеджера авторизации
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Маршрут главной страницы
@app.route('/')
def index():
    gyms = Gym.query.all()
    subscription_types = SubscriptionType.query.all()
    return render_template('index.html', gyms=gyms, subscription_types=subscription_types)

# Маршрут страницы фитнес-центра
@app.route('/gym/<int:gym_id>')
def gym(gym_id):
    gym = Gym.query.get_or_404(gym_id)
    return render_template('gym.html', gym=gym)

# Маршрут страницы карты
@app.route('/map')
def map():
    gyms = Gym.query.all()
    return render_template('map.html', gyms=gyms)

# Маршрут страницы авторизации
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

# Маршрут страницы регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Маршрут страницы выхода из системы
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

# Маршрут для покупки подписки
@app.route('/subscribe', methods=['GET', 'POST'])
@login_required
def subscribe():
    if request.method == 'POST':
        # Обработать логику подписки здесь
        # ...
        return redirect(url_for('index'))
    return render_template('subscribe.html')

# Маршрут для просмотра списка тренировок
@app.route('/workouts')
@login_required
def workouts():
    workouts = current_user.workouts.all()
    trainers = Trainer.query.all()
    workout_types = WorkoutType.query.all()
    return render_template('workouts.html', workouts=workouts, trainers=trainers, workout_types=workout_types)

@app.route('/gym/<int:gym_id>', methods=['GET'])
def gym_detail(gym_id):
    # Retrieve the gym details based on the gym_id
    gym = next((g for g in gyms if g.id == gym_id), None)
    if gym:
        return render_template('gym_detail.html', gym=gym)
    else:
        return redirect(url_for('workouts'))

