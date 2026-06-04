import json
import logging

import stripe
from flask import current_app
from google.cloud.firestore_v1 import ArrayUnion, Increment

from extensions import get_db

logger = logging.getLogger(__name__)


class GiftService:
    COLLECTION = 'gifts'

    @classmethod
    def get_all(cls) -> list[dict]:
        db = get_db()
        docs = [{'id': d.id, **d.to_dict()} for d in db.collection(cls.COLLECTION).stream()]
        return sorted(docs, key=lambda g: g.get('order', 999))

    @classmethod
    def get_one(cls, gift_id: str) -> dict | None:
        db = get_db()
        doc = db.collection(cls.COLLECTION).document(gift_id).get()
        return {'id': doc.id, **doc.to_dict()} if doc.exists else None

    @classmethod
    def create_checkout_session(
        cls,
        gift_id: str,
        guest_name: str,
        amount_mxn: float,
        show_name: bool,
        base_url: str,
    ) -> str:
        stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
        gift = cls.get_one(gift_id)
        if not gift:
            raise ValueError('Gift not found')

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'mxn',
                    'product_data': {
                        'name': gift['title'],
                        'description': gift.get('description', ''),
                    },
                    'unit_amount': int(round(amount_mxn * 100)),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f'{base_url}/gifts/success?session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url=f'{base_url}/gifts?cancelled=1',
            metadata={
                'gift_id': gift_id,
                'guest_name': guest_name,
                'show_name': 'true' if show_name else 'false',
                'amount_mxn': str(amount_mxn),
            },
        )
        return session.url

    @classmethod
    def handle_webhook(cls, payload: bytes, sig_header: str) -> None:
        stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
        # Verify signature — raises SignatureVerificationError if invalid
        stripe.Webhook.construct_event(
            payload, sig_header, current_app.config['STRIPE_WEBHOOK_SECRET']
        )
        # Parse raw JSON directly to avoid StripeObject API differences across SDK versions
        body = json.loads(payload)
        event_type = body.get('type')
        logger.info('Stripe event received: %s', event_type)

        if event_type == 'checkout.session.completed':
            meta = body.get('data', {}).get('object', {}).get('metadata', {})
            gift_id = meta.get('gift_id')
            guest_name = meta.get('guest_name', '')
            show_name = meta.get('show_name') == 'true'
            amount_mxn = float(meta.get('amount_mxn', 0))
            logger.info(
                'Checkout completed — gift_id=%s guest=%s amount=%.2f show_name=%s',
                gift_id, guest_name, amount_mxn, show_name,
            )

            if gift_id and amount_mxn > 0:
                cls._record_contribution(gift_id, guest_name, show_name, amount_mxn)
            else:
                logger.warning('Webhook skipped: missing gift_id or zero amount — meta=%s', meta)

    @classmethod
    def _record_contribution(
        cls, gift_id: str, guest_name: str, show_name: bool, amount_mxn: float
    ) -> None:
        db = get_db()
        ref = db.collection(cls.COLLECTION).document(gift_id)
        contributor = guest_name if show_name else 'Anónimo'

        # Verify document exists before attempting field-transform update
        if not ref.get().exists:
            logger.error('_record_contribution: gift document %r not found in Firestore', gift_id)
            raise ValueError(f'Gift {gift_id!r} not found')

        ref.update({
            'amount_funded': Increment(amount_mxn),
            'contributors': ArrayUnion([contributor]),
        })
        logger.info('Contribution recorded: gift_id=%s contributor=%s amount=%.2f', gift_id, contributor, amount_mxn)

        # Mark fully funded if target reached
        doc = ref.get()
        data = doc.to_dict()
        if data.get('amount_funded', 0) >= data.get('price', float('inf')):
            ref.update({'is_funded': True})
            logger.info('Gift %s marked as fully funded', gift_id)
