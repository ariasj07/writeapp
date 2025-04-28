from functools import wraps
from flask import session, render_template, redirect, url_for

def check_user(func):
    @wraps(func) # <- copia el nombre e info de func (original) en wrapper
    def wrapper(*args, **kwargs):
        user = session.get("user_id")
        if not user:
            return redirect(url_for('user.register'))
        else:
            print(user)
            return func(*args, **kwargs)
    return wrapper