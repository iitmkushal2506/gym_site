import os
from app import create_app
from app.extensions import db
from app.models import Admin
from seed import seed_database

# WSGI Application entrypoint for Gunicorn / Render
env = os.environ.get('FLASK_ENV', 'production')
app = create_app(env)

# Initialize database safely on startup
with app.app_context():
    try:
        db.create_all()
        if Admin.query.count() == 0:
            seed_database(app)
    except Exception as e:
        app.logger.warning(f"Startup DB initialization notice: {e}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
