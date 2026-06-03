from extensions import get_db


class GuestService:
    COLLECTION = 'guests'

    @classmethod
    def get_all(cls) -> list[dict]:
        db = get_db()
        docs = db.collection(cls.COLLECTION).stream()
        results = [{'id': d.id, **d.to_dict()} for d in docs]
        results.sort(key=lambda x: x.get('name', ''))
        return results

    @classmethod
    def get_by_id(cls, doc_id: str) -> dict | None:
        db = get_db()
        doc = db.collection(cls.COLLECTION).document(doc_id).get()
        return {'id': doc.id, **doc.to_dict()} if doc.exists else None
