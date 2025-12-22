from sqlalchemy import or_
from database.models import Applicant, Job, Company
from database.database import get_db_session


class SearchQueries:
    def __init__(self):
        self.db = get_db_session()

    def global_search(self, query: str):
        search_filter = f"{query}%"

        # Ludzie
        people = self.db.query(Applicant).filter(
            or_(
                Applicant.name.ilike(search_filter),
                Applicant.surname.ilike(search_filter)
            )
        ).all()

        # Oferty pracy
        jobs = self.db.query(Job).filter(
            or_(
                Job.title.ilike(search_filter)
            )
        ).all()

        # Firmy
        companies = self.db.query(Company).filter(
            or_(
                Company.name.ilike(search_filter)
            )
        ).all()

        return {
            "people": people,
            "jobs": jobs,
            "companies": companies
        }
