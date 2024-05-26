import sqlite3

conn = sqlite3.connect('instance/gym.db')

# Установка размера кэша SQLite на 10 МБ
conn.execute("PRAGMA cache_size = -10000;")

c = conn.cursor()

# Создание таблицы Gyms
c.execute('''CREATE TABLE IF NOT EXISTS Gyms
             (gym_id INTEGER PRIMARY KEY,
              name TEXT,
              address TEXT,
              latitude REAL,
              longitude REAL,
              description TEXT,
              amenities TEXT)''')

# Создание таблицы SubscriptionOptions
c.execute('''CREATE TABLE IF NOT EXISTS SubscriptionOptions
             (option_id INTEGER PRIMARY KEY,
              name TEXT,
              description TEXT,
              duration INTEGER,
              price REAL)''')

# Создание таблицы Users
c.execute('''CREATE TABLE IF NOT EXISTS Users
             (user_id INTEGER PRIMARY KEY,
              username TEXT,
              email TEXT,
              password_hash TEXT,
              subscription_id INTEGER,
              FOREIGN KEY (subscription_id) REFERENCES Subscriptions(subscription_id))''')

# Создание таблицы Subscriptions
c.execute('''CREATE TABLE IF NOT EXISTS Subscriptions
             (subscription_id INTEGER PRIMARY KEY,
              user_id INTEGER,
              option_id INTEGER,
              start_date TEXT,
              end_date TEXT,
              is_active INTEGER,
              FOREIGN KEY (user_id) REFERENCES Users(user_id),
              FOREIGN KEY (option_id) REFERENCES SubscriptionOptions(option_id))''')

# Создание таблицы Trainers
c.execute('''CREATE TABLE IF NOT EXISTS Trainers
             (trainer_id INTEGER PRIMARY KEY,
              name TEXT,
              specialization TEXT,
              description TEXT,
              gym_id INTEGER,
              FOREIGN KEY (gym_id) REFERENCES Gyms(gym_id))''')

# Создание таблицы Workouts
c.execute('''CREATE TABLE IF NOT EXISTS Workouts
             (workout_id INTEGER PRIMARY KEY,
              name TEXT,
              description TEXT,
              duration INTEGER,
              difficulty TEXT,
              gym_id INTEGER,
              trainer_id INTEGER,
              FOREIGN KEY (gym_id) REFERENCES Gyms(gym_id),
              FOREIGN KEY (trainer_id) REFERENCES Trainers(trainer_id))''')

conn.commit()
conn.close()
