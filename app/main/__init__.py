from flask import Blueprint

from app.modles import Permission

main = Blueprint('main', __name__)

from . import views, errors

@main.app_context_processor
def inject_permission():
    return dict(Permission=Permission)