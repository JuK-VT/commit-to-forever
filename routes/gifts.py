import logging

import stripe
from flask import (Blueprint, current_app, flash, redirect,
                   render_template, request, session, url_for)

from services.gift_service import GiftService

logger = logging.getLogger(__name__)

gifts_bp = Blueprint('gifts', __name__)

MIN_PARTIAL_MXN = 50.0


@gifts_bp.route('/gifts')
def gifts():
    if not session.get('guest_name'):
        flash('Debes acceder antes de ver la lista de regalos.', 'error')
        return redirect(url_for('auth.login'))

    cancelled = request.args.get('cancelled') == '1'
    return render_template(
        'gifts.html',
        gifts=GiftService.get_all(),
        cancelled=cancelled,
        stripe_pk=current_app.config['STRIPE_PUBLISHABLE_KEY'],
    )


@gifts_bp.route('/gifts/<gift_id>/checkout', methods=['POST'])
def checkout(gift_id):
    if not session.get('guest_name'):
        flash('Debes acceder para realizar un regalo.', 'error')
        return redirect(url_for('auth.login'))

    gift = GiftService.get_one(gift_id)
    if not gift or gift.get('is_funded'):
        flash('Este regalo ya no está disponible.', 'error')
        return redirect(url_for('gifts.gifts'))

    show_name = request.form.get('show_name') == 'on'

    if gift.get('allow_partial'):
        try:
            amount_mxn = float(request.form.get('amount', 0))
        except ValueError:
            amount_mxn = MIN_PARTIAL_MXN
        remaining = gift['price'] - gift.get('amount_funded', 0)
        amount_mxn = max(MIN_PARTIAL_MXN, min(amount_mxn, remaining))
    else:
        amount_mxn = float(gift['price'])

    try:
        url = GiftService.create_checkout_session(
            gift_id=gift_id,
            guest_name=session['guest_name'],
            amount_mxn=amount_mxn,
            show_name=show_name,
            base_url=request.host_url.rstrip('/'),
        )
        return redirect(url)
    except Exception:
        flash('Hubo un problema al procesar tu regalo. Inténtalo de nuevo.', 'error')
        return redirect(url_for('gifts.gifts'))


@gifts_bp.route('/gifts/success')
def success():
    if not session.get('guest_name'):
        return redirect(url_for('auth.login'))
    return render_template('gifts_success.html')


@gifts_bp.route('/gifts/webhook', methods=['POST'])
def webhook():
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature', '')

    try:
        GiftService.handle_webhook(payload, sig_header)
        return '', 200
    except stripe.SignatureVerificationError as e:
        logger.warning('Stripe webhook signature invalid: %s', e)
        return '', 400
    except Exception as e:
        logger.exception('Stripe webhook processing failed: %s', e)
        return '', 500
