from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from services.rsvp_service import RsvpService

rsvp_bp = Blueprint('rsvp', __name__)


@rsvp_bp.route('/rsvp', methods=['GET', 'POST'])
def rsvp():
    if not session.get('guest_name'):
        flash('Debes acceder antes de confirmar tu asistencia.', 'error')
        return redirect(url_for('auth.login'))

    max_plus_ones = session.get('max_plus_ones', 0)
    max_guests = 1 + max_plus_ones

    if request.method == 'POST':
        attending = request.form.get('attending') == 'yes'
        guest_count = min(int(request.form.get('guest_count') or 1), max_guests)
        dietary      = request.form.get('dietary', '').strip()
        message      = request.form.get('message', '').strip()
        song_request = request.form.get('song_request', '').strip()
        RsvpService.save(
            guest_name=session['guest_name'],
            attending=attending,
            guest_count=guest_count,
            dietary=dietary,
            message=message,
            song_request=song_request,
        )
        return render_template('rsvp.html', confirmed=True,
                               attending=attending, max_guests=max_guests,
                               existing=None)

    existing = RsvpService.get_by_guest(session['guest_name'])
    return render_template('rsvp.html', confirmed=False,
                           max_guests=max_guests, existing=existing)
