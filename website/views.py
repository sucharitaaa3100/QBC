from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def landing_page():
    print("Its here")
    return render_template("landing_page.html", user=current_user)

@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if(current_user.email == "qbc_admin@fastmail.com"):
        return render_template("admin_dashboard.html")
    else:    
        return render_template("user_dashboard.html")

@views.route('/about')
def about():
    return render_template('landing_page.html') #about the project

