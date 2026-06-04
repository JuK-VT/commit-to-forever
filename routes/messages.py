from flask import Blueprint, jsonify, request, session

from services.messages_service import MessagesService

messages_bp = Blueprint('messages', __name__, url_prefix='/mensajes')


@messages_bp.post('/add')
def add_message():
    if 'guest_name' not in session:
        return jsonify({'error': 'No autenticado'}), 401

    data = request.get_json(silent=True) or {}
    text = data.get('message', '').strip()
    if not text:
        return jsonify({'error': 'El mensaje no puede estar vacío'}), 400

    guest_name = session['guest_name']
    MessagesService.add(guest_name=guest_name, message=text)
    return jsonify({'ok': True, 'guest_name': guest_name, 'message': text}), 201
