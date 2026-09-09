import os
import click
from app import create_app
from app.extensions import db
from app.models import Admin
from seed import seed_database

env = os.environ.get('FLASK_ENV', 'development')
app = create_app(env)


@app.cli.command("seed-db")
def seed_db_command():
    """Seed the database with realistic demo data."""
    click.echo("Seeding Kushal's Gym Site database...")
    seed_database(app)
    click.echo("Seeding completed successfully!")


@app.cli.command("create-admin")
@click.option("--username", prompt=True, help="Admin username")
@click.option("--email", prompt=True, help="Admin email address")
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True, help="Admin password")
def create_admin_command(username, email, password):
    """Create a new admin user securely."""
    with app.app_context():
        existing = Admin.query.filter((Admin.username == username) | (Admin.email == email)).first()
        if existing:
            click.echo(f"Error: Admin with username '{username}' or email '{email}' already exists.")
            return

        admin = Admin(username=username, email=email.lower())
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        click.echo(f"Admin user '{username}' created successfully!")


# Auto-seed on first start if tables don't exist
with app.app_context():
    try:
        db.create_all()
        if Admin.query.count() == 0:
            seed_database(app)
    except Exception as e:
        app.logger.warning(f"Startup DB initialization notice: {e}")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
