from datetime import datetime, timezone

from extensions import get_db


class MessagesService:
    COLLECTION = 'messages'

    @classmethod
    def get_all(cls) -> list[dict]:
        db = get_db()
        docs = db.collection(cls.COLLECTION).stream()
        results = [{'id': d.id, **d.to_dict()} for d in docs]
        results.sort(
            key=lambda x: x.get('created_at') or datetime.min.replace(tzinfo=timezone.utc),
            reverse=True,
        )
        return results

    @classmethod
    def add(cls, guest_name: str, message: str) -> str:
        db = get_db()
        _, ref = db.collection(cls.COLLECTION).add({
            'guest_name': guest_name,
            'message': message,
            'created_at': datetime.now(timezone.utc),
        })
        return ref.id
