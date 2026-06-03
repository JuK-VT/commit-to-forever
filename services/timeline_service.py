from extensions import get_db


class TimelineService:
    COLLECTION = 'timeline'

    @classmethod
    def get_all(cls) -> list[dict]:
        db = get_db()
        docs = db.collection(cls.COLLECTION).stream()
        results = [{'id': d.id, **d.to_dict()} for d in docs]
        results.sort(key=lambda x: x.get('order', 0))
        return results
