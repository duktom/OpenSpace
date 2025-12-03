import logging

from fastapi import Query
from fastapi import HTTPException

from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from database import db_session_scope
from database import MissingDatabaseError


logger = logging.getLogger(__name__)


class BaseQueries:

    def __init__(self, model):
        self.model = model

    def get_all(self):
        try:
            with db_session_scope(commit=False) as session:
                return session.query(self.model).all()
        except MissingDatabaseError:
            logger.error("Database for provided object does not exist")
            raise HTTPException(404)

    def get_all_with_relations(self, relations: list = []):
        try:
            with db_session_scope(commit=False) as session:
                query = session.query(self.model)
                if relations:
                    query = self.add_relation_args(relations, query)
                return query.all()
        except MissingDatabaseError:
            logger.error("Database for provided object does not exist")
            raise HTTPException(404)

    def get_by_id_with_relations(self, id: int, relations: list = []):
        try:
            with db_session_scope(commit=False) as session:
                query = session.query(self.model).filter(self.model.id == id)
                if relations:
                    query = self.add_relation_args(relations, query)
                response = query.first()
                if response is None:
                    raise HTTPException(404)
                return response
        except MissingDatabaseError:
            logger.error("Database for provided object does not exist")
            raise HTTPException(404)

    def get_by_id(self, id: int):
        try:
            with db_session_scope(commit=False) as session:
                return (
                    session.query(self.model)
                    .filter(self.model.id == id)
                    .first()
                )
        except MissingDatabaseError:
            logger.error("Database for provided object does not exist")
            raise HTTPException(404)

    def post_record(self, dataResponse: BaseModel):
        try:
            with db_session_scope(commit=True) as session:
                session.add(self.model(**dataResponse.__dict__))
                return dataResponse
        except IntegrityError as e:
            logger.warning(
                f"{self.model.__tablename__} - One of the foreign keys might cause an error."
            )
            logger.error(e)
            raise HTTPException(409)
        except MissingDatabaseError:
            logger.error("Database for provided object does not exist")
            raise HTTPException(404)

    def update_record(self, model_obj: BaseModel):
        try:
            with db_session_scope(commit=True) as session:
                data = (
                    session.query(self.model)
                    .filter(self.model.id == model_obj.id)
                    .first()
                )
                if data is None:
                    raise HTTPException(404)
                session.delete(data)
                session.add(self.model(**model_obj.__dict__))
                return model_obj
        except IntegrityError:
            logger.warning(
                f"{self.model.__tablename__} - One of the foreign keys might cause an error."
            )
            raise HTTPException(409)
        except MissingDatabaseError:
            logger.error("Database for provided object does not exist")
            raise HTTPException(404)

    def delete_record(self, id: int):
        try:
            with db_session_scope(commit=True) as session:
                data = (
                    session.query(self.model)
                    .filter(self.model.id == id)
                    .first()
                )
                if data is None:
                    raise HTTPException(404)
                session.delete(data)
                return (data)
        except MissingDatabaseError:
            logger.error("Database for provided object does not exist")
            raise HTTPException(404)

    def add_relation_args(self, relations: list, query: Query):
        for relation in relations:
            query = query.options(relation)
        return query
