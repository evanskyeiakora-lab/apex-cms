from app.extensions import db


class BaseService:
    model = None

    @classmethod
    def get_all(cls):
        return cls.model.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.model.query.get_or_404(id)

    @classmethod
    def create(cls, obj):
        db.session.add(obj)
        db.session.commit()
        return obj

    @classmethod
    def update(cls):
        db.session.commit()

    @classmethod
    def delete(cls, obj):
        db.session.delete(obj)
        db.session.commit()