from functools import wraps
from flask import abort, redirect, url_for, flash # Import flash
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function

def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_admin:
            flash("Administrators do not have access to user-specific pages.", "warning") # Added flash message
            return redirect(url_for("views.admin_dashboard")) # Redirect admins to their dashboard
        return f(*args, **kwargs)
    return decorated_function

