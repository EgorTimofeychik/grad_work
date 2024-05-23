from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Gym, SubscriptionType, Subscription, Workout, Trainer, WorkoutType

# Создание экземпляра Flask
app = Flask(__name__)
app.config.from_object('config')

# Инициализация базы данных SQLAlchemy
db.init_app(app)

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
        if user and user.check_password(request.form['password']):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

# Маршрут страницы выхода из системы
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

# Маршрут для покупки подписки
@app.route('/subscribe', methods=['POST'])
@login_required
def subscribe():
    gym_id = request.form['gym_id']
    subscription_type_id = request.form['subscription_type_id']
    gym = Gym.query.get(gym_id)
    subscription_type = SubscriptionType.query.get(subscription_type_id)
    subscription = Subscription(user=current_user, gym=gym, subscription_type=subscription_type)
    db.session.add(subscription)
    db.session.commit()
    flash('Subscription purchased successfully.', 'success')
    return redirect(url_for('index'))

# Маршрут для просмотра списка тренировок
@app.route('/workouts')
@login_required
def workouts():
    workouts = current_user.workouts.all()
    trainers = Trainer.query.all()
    workout_types = WorkoutType.query.all()
    return render_template('workouts.html', workouts=workouts, trainers=trainers, workout_types=workout_types)

# Маршрут для бронирования тренировки
@app.route('/book_workout', methods=['POST'])
@login_required
def book_workout():
    workout_type_id = request.form['workout_type_id']
    trainer_id = request.form['trainer_id']
    start_time = request.form['start_time']
    workout_type = WorkoutType.query.get(workout_type_id)
    trainer = Trainer.query.get(trainer_id)
    workout = Workout(user=current_user, workout_type=workout_type, trainer=trainer, start_time=start_time)
    db.session.add(workout)
    db.session.commit()
    flash('Workout booked successfully.', 'success')
    return redirect(url_for('workouts'))

# Точка входа приложения
if __name__ == '__main__':
    app.run(debug=True)