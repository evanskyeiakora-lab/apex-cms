from app.models import (
    User,
    News,
    Event,
    Gallery,
    HeroSlide,
    Member,
    Page
)


class DashboardService:

    @staticmethod
    def get_statistics():

        return {

            "users": User.query.count(),

            "news": News.query.count(),

            "events": Event.query.count(),

            "gallery": Gallery.query.count(),

            "hero": HeroSlide.query.count(),

            "members": Member.query.count(),

            "pages": Page.query.count()

        }

    @staticmethod
    def recent_news(limit=5):

        return (

            News.query

            .order_by(News.created_at.desc())

            .limit(limit)

            .all()

        )

    @staticmethod
    def upcoming_events(limit=5):

        return (

            Event.query

            .order_by(Event.start_date.asc())

            .limit(limit)

            .all()

        )