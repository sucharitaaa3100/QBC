from flask import Blueprint, render_template, request, flash, redirect, url_for
import random
from flask_mailman import Mail, EmailMessage
from .models import User
 
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
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
    # return login page
    return # verify page

def generate_verification_code():
    return str(random.randint(100000, 999999))