from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, current_app
from flask_login import login_required, current_user
from .models import User
views = Blueprint('views', __name__)

@views.landing_page('/',methods=['GET', 'POST'])
def landing_page():
    if current_user.is_authenticated:
       return # dashboard 
    return # landing page

@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if(current_user.mail == "admin_qbc@fastmail.com"):
        return #admin dasboard
    else:    
        return #user dashboard

