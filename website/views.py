from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
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
        return #admin dashboard
    else:    
        return #user dashboard

@views.route('/about')
def about():
    return #about the project

