from data.wedding import GIFTS
from extensions import get_db


class GiftService:
    COLLECTION = 'gifts'

    @classmethod
    def get_all(cls):
        db = get_db()
        live = {doc.id: doc.to_dict() for doc in db.collection(cls.COLLECTION).stream()}
        return [{**gift, **live.get(str(gift['id']), {})} for gift in GIFTS]

    @classmethod
    def claim(cls, gift_id: int, guest_name: str) -> None:
        db = get_db()
        db.collection(cls.COLLECTION).document(str(gift_id)).set(
            {'claimed': True, 'claimed_by': guest_name},
            merge=True,
        )
