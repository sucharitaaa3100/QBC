from flask import Blueprint, render_template, request, flash, redirect, url_for
import random
from flask_mailman import Mail, EmailMessage
from .models import User
 
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # if not verified redirect to verify
    # return dashboard is session present
    return #login page


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    # return verification
    return #signup page

@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    return #landing_page

@auth.route('/verify-email', methods=['GET', 'POST'])
def verify_email():
    # if verified return login page
    return # else verify page

def generate_verification_code():
    return str(random.randint(100000, 999999))

@auth.route('re-verify-email', methods=['GET', 'POST'])
def resend_verification_code():
    # redirect to verify_email
    return #verify_email