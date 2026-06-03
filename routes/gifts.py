from flask import Blueprint, flash, redirect, render_template, session, url_for

from data.wedding import WEDDING
from services.gift_service import GiftService

gifts_bp = Blueprint('gifts', __name__)


@gifts_bp.route('/gifts')
def gifts():
    if not session.get('guest_name'):
        flash('Debes acceder antes de ver la lista de regalos.', 'error')
        return redirect(url_for('auth.login'))

    return render_template('gifts.html', gifts=GiftService.get_all(), wedding=WEDDING)
