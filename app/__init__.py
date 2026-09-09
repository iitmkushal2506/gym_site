import os
from datetime import datetime
from flask import Flask, render_template
from app.config import config_by_name
from app.extensions import db, login_manager, csrf, mail


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name['default']))

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)

    # Register Blueprints
    from app.routes.main import main_bp
    from app.routes.booking import booking_bp
    from app.routes.contact import contact_bp
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(auth_bp, url_prefix='/admin')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Global context processors for Jinja templates
    @app.context_processor
    def inject_global_vars():
        return {
            'current_year': datetime.utcnow().year,
            'gym_name': app.config.get('GYM_NAME', 'IRONFORGE FITNESS'),
            'gym_tagline': app.config.get('GYM_TAGLINE', 'BUILD STRONGER. LIVE STRONGER.'),
            'gym_phone': app.config.get('GYM_PHONE', '+91 98765 43210'),
            'gym_email': app.config.get('GYM_EMAIL', 'info@ironforgefitness.com'),
            'gym_address': app.config.get('GYM_ADDRESS', '42 Titan Avenue, Platinum Heights, Metro City, 560001'),
            'gym_whatsapp': app.config.get('GYM_WHATSAPP', '919876543210'),
            'gym_instagram': app.config.get('GYM_INSTAGRAM', 'https://instagram.com/ironforgefitness'),
            'ga_tracking_id': app.config.get('GA_TRACKING_ID', '')
        }

    # Custom Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    return app
