import os
from datetime import datetime
from flask import Flask, render_template
from app.config import config_by_name
from app.extensions import db, login_manager, csrf, mail


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    flask_app = Flask(__name__)
    config_obj = config_by_name.get(config_name, config_by_name['default'])
    flask_app.config.from_object(config_obj)

    # Initialize extensions
    db.init_app(flask_app)
    login_manager.init_app(flask_app)
    csrf.init_app(flask_app)
    mail.init_app(flask_app)

    # Register Blueprints
    from app.routes.main import main_bp
    from app.routes.booking import booking_bp
    from app.routes.contact import contact_bp
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp

    flask_app.register_blueprint(main_bp)
    flask_app.register_blueprint(booking_bp)
    flask_app.register_blueprint(contact_bp)
    flask_app.register_blueprint(auth_bp, url_prefix='/admin')
    flask_app.register_blueprint(admin_bp, url_prefix='/admin')

    # Global context processors for Jinja templates
    @flask_app.context_processor
    def inject_global_vars():
        return {
            'current_year': datetime.utcnow().year,
            'gym_name': flask_app.config.get('GYM_NAME', "KUSHAL'S GYM SITE"),
            'gym_tagline': flask_app.config.get('GYM_TAGLINE', 'BUILD STRONGER. LIVE STRONGER.'),
            'gym_phone': flask_app.config.get('GYM_PHONE', '+91 98XXX XXXXX'),
            'gym_email': flask_app.config.get('GYM_EMAIL', 'contact@kushalgym.demo'),
            'gym_address': flask_app.config.get('GYM_ADDRESS', '123 Fitness Boulevard, Sector XX, Metro City, 000000'),
            'gym_whatsapp': flask_app.config.get('GYM_WHATSAPP', '9198XXXXXXXX'),
            'gym_instagram': flask_app.config.get('GYM_INSTAGRAM', 'https://instagram.com/yourgymhandle'),
            'ga_tracking_id': flask_app.config.get('GA_TRACKING_ID', '')
        }

    # Custom Error Handlers
    @flask_app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @flask_app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    return flask_app


# Expose default WSGI 'app' object so both `gunicorn app:app`, `gunicorn wsgi:app`, and `gunicorn run:app` work instantly
app = create_app(os.environ.get('FLASK_ENV', 'production'))

with app.app_context():
    try:
        db.create_all()
        from app.models import Admin
        if Admin.query.count() == 0:
            from seed import seed_database
            seed_database(app)
    except Exception as e:
        pass
