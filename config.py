import os

class Config:
    # Базовая конфигурация
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///gym.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Конфигурация пользователя
    LOGIN_VIEW = 'auth.login'
    LOGIN_MESSAGE = 'Please log in to access this page.'

    # Google Maps 
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY') or \
        'your_google_maps_api_key'

    # Конфигурация тренажерного зала
    GYM_SUBSCRIPTION_TYPES = ['monthly', 'yearly', 'family']
    GYM_SUBSCRIPTION_PRICES = {
        'monthly': 50,
        'yearly': 500,
        'family': 100
    }
    GYM_LIST = [
        {
            'name': 'Gym A',
            'lat': 37.7749,
            'lng': -122.4194,
            'address': '123 Main St'
        },
        {
            'name': 'Gym B',
            'lat': 40.7128,
            'lng': -74.0060,
            'address': '456 Broadway'
        },
        
    ]

    # Конфигурация тренировки
    WORKOUT_TYPES = ['strength', 'cardio', 'yoga']
    TRAINER_LIST = [
        {
            'name': 'John Doe',
            'specialty': 'Strength Training',
            'hourly_rate': 75
        },
        {
            'name': 'Jane Smith',
            'specialty': 'Yoga',
            'hourly_rate': 60
        },
    ]
