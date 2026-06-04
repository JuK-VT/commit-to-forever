from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from data.wedding import WEDDING
from services.auth_service import AuthService
from services.guest_service import GuestService

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    guests = GuestService.get_all()

    if request.method == 'POST':
        guest_id = request.form.get('guest_id', '').strip()
        password = request.form.get('password', '')

        if not guest_id or not password:
            flash('Por favor, selecciona tu nombre y escribe una contraseña.', 'error')
            return render_template('login.html', wedding=WEDDING, guests=guests)

        guest = GuestService.get_by_id(guest_id)
        if not guest:
            flash('Nombre no encontrado en la lista de invitados.', 'error')
            return render_template('login.html', wedding=WEDDING, guests=guests)

        success, reason = AuthService.register_or_login(guest['name'], password)

        if success:
            session['guest_name'] = guest['name']
            session['max_plus_ones'] = guest.get('max_plus_ones', 0)
            if reason == 'registered':
                flash(f'¡Bienvenido/a, {guest["name"]}! Tu acceso ha sido creado.', 'success')
            else:
                flash(f'¡Bienvenido/a de nuevo, {guest["name"]}!', 'success')
            return redirect(url_for('main.index'))

        flash('Contraseña incorrecta. Inténtalo de nuevo.', 'error')

    return render_template('login.html', wedding=WEDDING, guests=guests)


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))
