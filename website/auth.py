from flask import Blueprint, render_template, request, flash, redirect, url_for
import random
from flask_mailman import Mail, EmailMessage
from .models import User
 
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    return

@auth.route('/verify-email', methods=['GET', 'POST'])
def verify_email():
    return

def generate_verification_code():
    return str(random.randint(100000, 999999))