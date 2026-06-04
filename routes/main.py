from flask import Blueprint, render_template

from services.messages_service import MessagesService
from services.timeline_service import TimelineService

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    try:
        timeline = TimelineService.get_all()
        messages = MessagesService.get_all()
    except RuntimeError:
        timeline = []
        messages = []
    return render_template('index.html', timeline=timeline, messages=messages)
