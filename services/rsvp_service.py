from extensions import get_db


class RsvpService:
    COLLECTION = 'rsvps'

    @classmethod
    def get_by_guest(cls, guest_name: str) -> dict | None:
        """Return the existing RSVP document for this guest, or None."""
        db = get_db()
        docs = (
            db.collection(cls.COLLECTION)
            .where('guest_name', '==', guest_name)
            .limit(1)
            .stream()
        )
        results = list(docs)
        if not results:
            return None
        doc = results[0]
        return {'id': doc.id, **doc.to_dict()}

    @classmethod
    def save(
        cls,
        guest_name: str,
        attending: bool,
        guest_count: int,
        dietary: str,
        message: str,
        song_request: str = '',
    ) -> None:
        """Upsert: update the guest's existing RSVP or create one if absent."""
        data = {
            'guest_name': guest_name,
            'attending': attending,
            'guest_count': guest_count,
            'dietary': dietary,
            'message': message,
            'song_request': song_request,
        }
        db = get_db()
        existing = cls.get_by_guest(guest_name)
        if existing:
            db.collection(cls.COLLECTION).document(existing['id']).set(data)
        else:
            db.collection(cls.COLLECTION).add(data)
