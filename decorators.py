from flask import redirect
from flask import url_for
from flask import session
from flask import flash

from functools import wraps


def login_required_custom(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'team_id' in session:
            return func(*args, **kwargs)
        else:
            flash('Please login to visit this page', 'danger')
            return redirect(url_for('team_blueprint.login'))

    return wrapper
