from flask import Blueprint, render_template

gifts_bp = Blueprint('gifts', __name__)


@gifts_bp.route('/gifts')
def gifts():
    return render_template('gifts.html')
