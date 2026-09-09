import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    """Base application configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'ironforge-fitness-ultra-secret-key-2026-production')
    
    # Database URL handling with PostgreSQL and SQLite fallback
    raw_db_url = os.environ.get('DATABASE_URL')
    if raw_db_url:
        # Fix Render/Heroku postgres:// schema for SQLAlchemy 2+
        if raw_db_url.startswith('postgres://'):
            raw_db_url = raw_db_url.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = raw_db_url
    else:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'ironforge.db')}"
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security & CSRF
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    
    # Mail settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() in ('true', '1', 't')
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'False').lower() in ('true', '1', 't')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'notifications@ironforgefitness.com')
    ADMIN_NOTIFICATION_EMAIL = os.environ.get('ADMIN_NOTIFICATION_EMAIL', 'gymadmin@ironforgefitness.com')
    
    # Business Brand Defaults
    GYM_NAME = os.environ.get('GYM_NAME', 'IRONFORGE FITNESS')
    GYM_TAGLINE = os.environ.get('GYM_TAGLINE', 'BUILD STRONGER. LIVE STRONGER.')
    GYM_PHONE = os.environ.get('GYM_PHONE', '+91 98765 43210')
    GYM_EMAIL = os.environ.get('GYM_EMAIL', 'info@ironforgefitness.com')
    GYM_ADDRESS = os.environ.get('GYM_ADDRESS', '42 Titan Avenue, Platinum Heights, Metro City, 560001')
    GYM_WHATSAPP = os.environ.get('GYM_WHATSAPP', '919876543210')
    GYM_INSTAGRAM = os.environ.get('GYM_INSTAGRAM', 'https://instagram.com/ironforgefitness')
    
    # Google Analytics ID
    GA_TRACKING_ID = os.environ.get('GA_TRACKING_ID', '')


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True


config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig if os.environ.get('FLASK_ENV') == 'development' else ProductionConfig
}
