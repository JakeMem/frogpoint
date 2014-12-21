from functools import wraps

from flask import g, render_template, abort
from flask_login import login_required


def render_to(tpl):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            out = func(*args, **kwargs)
            if out is None:
                out = {}
            if isinstance(out, dict):
                out = render_template(tpl, **out)
            return out
        return wrapper
    return decorator


def admin_required(func):
    @login_required
    @wraps(func)
    def wrapper(*args, **kwargs):
        if g.user.is_superuser:
            return func(*args, **kwargs)
        else:
            return abort(401, 'Un-authorized access')
    return wrapper
