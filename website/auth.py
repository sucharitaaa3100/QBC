from flask import Blueprint, render_template, request, flash, redirect, url_for, session, current_app
import random
from flask_mailman import EmailMessage
from datetime import datetime, date
from .models import User
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, mail
import os
import re

auth = Blueprint('auth', __name__)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        user = User.query.filter_by(email=email).first()

        if not email or not password:
            flash('Please enter both email and password.', category='error')
            return render_template('login.html', user=current_user)

        if user:
            if not user.is_verified:
                flash('Please verify your email before logging in.', category='error')
                return redirect(url_for('auth.verify_email', email=email))

            # check_password_hash correctly handles the method used during hashing
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.dashboard'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Email doesn\'t exist', category='error')

    return render_template('login.html', user=current_user)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        full_name = request.form.get('full_name', '').strip()
        password1 = request.form.get('password1', '').strip()
        password2 = request.form.get('password2', '').strip()
        qualification = request.form.get('qualification', '').strip()
        dob_str = request.form.get('dob', '').strip()

        user = User.query.filter(User.email.ilike(email)).first()

        if user:
            flash('An account with this email already exists.', category='error')
        elif not EMAIL_REGEX.match(email):
            flash('Please enter a valid email address.', category='error')
        elif len(full_name) < 2:
            flash('Full name must be at least 2 characters long.', category='error')
        elif password2 != password1:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters long.', category='error')
        else:
            try:
                dob = None
                if dob_str:
                    dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
                
                verification_code = generate_verification_code()
                new_user = User(
                    email=email, 
                    full_name=full_name,
                    # Removed method='sha256'
                    password=generate_password_hash(password1), 
                    qualification=qualification,
                    dob=dob,
                    is_admin=False,
                    is_verified=False,
                    verification_code=verification_code
                )
                db.session.add(new_user)
                db.session.commit()

                msg = EmailMessage(
                    subject='QBC App: Email Verification',
                    body=f'Hi {full_name},\n\nThank you for signing up for QBC App! Your verification code is: {verification_code}\n\nPlease use this code to verify your email address and activate your account.\n\nBest regards,\nThe QBC Team',
                    to=[email],
                    from_email=current_app.config.get('MAIL_DEFAULT_SENDER', os.environ.get('MAIL_USERNAME'))
                )
                mail.send(msg)

                flash('Verification code sent! Please check your email and verify your account.', category='info')
                return redirect(url_for('auth.verify_email', email=email))

            except ValueError:
                flash("Invalid date format for Date of Birth. Please use YYYY-MM-DD.", category='error')
                db.session.rollback()
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred during signup: {str(e)}", category='error')

    return render_template('sign-up.html', user=current_user)

@auth.route('/verify-email', methods=['GET', 'POST'])
def verify_email():
    email = request.args.get('email', '').strip()
    user = User.query.filter_by(email=email).first()

    if not user:
        flash('User not found. Please sign up or check your email.', category='error')
        return redirect(url_for('auth.signup'))

    if user.is_verified:
        flash('Your email is already verified. Please log in.', category='success')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        code = request.form.get('code', '').strip()

        if user.verification_code == code:
            user.is_verified = True
            user.verification_code = None
            try:
                db.session.commit()
                flash('Email verified successfully! You can now log in.', category='success')
                return redirect(url_for('auth.login'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred during verification: {str(e)}", category='error')
        else:
            flash('Invalid verification code. Please try again.', category='error')

    return render_template('verify_email.html', email=email, user=current_user)

def generate_verification_code():
    """Generates a 6-digit numeric verification code."""
    return str(random.randint(100000, 999999))

@auth.route('/re-verify-email', methods=['GET'])
def resend_verification_code_page():
    """Renders the page to request resending verification code."""
    return render_template('resend_verification_code.html', user=current_user)

@auth.route('/resend-verification-code', methods=['POST'])
def resend_verification_code():
    email = request.form.get('email', '').strip()
    user = User.query.filter_by(email=email).first()

    if not email:
        flash('Please provide an email address to resend the code.', category='error')
        return redirect(url_for('auth.resend_verification_code_page'))

    if user:
        if user.is_verified:
            flash('Your email is already verified. Please log in.', category='info')
            return redirect(url_for('auth.login'))
        
        new_code = generate_verification_code()
        user.verification_code = new_code
        try:
            db.session.commit()

            msg = EmailMessage(
                subject='QBC App: Resend Email Verification',
                body=f'Hi {user.full_name},\n\nYour new verification code is: {new_code}\n\nPlease use this code to verify your email address.\n\nBest regards,\nThe QBC Team',
                to=[email],
                from_email=current_app.config.get('MAIL_DEFAULT_SENDER', os.environ.get('MAIL_USERNAME'))
            )
            mail.send(msg)

            flash('A new verification code has been sent to your email.', category='info')
            return redirect(url_for('auth.verify_email', email=email))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred while resending code: {str(e)}", category='error')
            return redirect(url_for('auth.login'))
    else:
        flash('No account found with that email address.', category='error')
        return redirect(url_for('auth.signup'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out.', category='success')
    return redirect(url_for('views.landing_page'))
