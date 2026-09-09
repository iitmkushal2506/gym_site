from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Admin
from app.forms import AdminLoginForm

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))

    form = AdminLoginForm()
    if form.validate_on_submit():
        user_input = form.username.data.strip()
        password = form.password.data

        # Allow login via username or email
        admin = Admin.query.filter(
            (Admin.username == user_input) | (Admin.email == user_input.lower())
        ).first()

        if admin and admin.check_password(password):
            login_user(admin, remember=form.remember_me.data)
            flash(f'Welcome back, {admin.username}!', 'success')
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/admin'):
                return redirect(next_page)
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username/email or password. Please check your credentials.', 'danger')

    return render_template('admin/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been securely signed out of the Admin Portal.', 'info')
    return redirect(url_for('auth.login'))
