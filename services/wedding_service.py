from extensions import get_db

_cache: dict | None = None


class WeddingService:
    COLLECTION = 'config'
    DOCUMENT = 'wedding'

    @classmethod
    def get(cls) -> dict:
        global _cache
        if _cache is None:
            db = get_db()
            doc = db.collection(cls.COLLECTION).document(cls.DOCUMENT).get()
            if not doc.exists:
                raise RuntimeError(
                    'Wedding config missing from Firestore — run dev/seed_wedding_once.py'
                )
            _cache = doc.to_dict()
        return _cache

    @classmethod
    def bust_cache(cls) -> None:
        global _cache
        _cache = None
