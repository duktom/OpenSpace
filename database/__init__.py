from contextlib import contextmanager

from database import database


@contextmanager
def db_session_scope(commit: bool = False):
    if not database.is_database_exist():
        raise MissingDatabaseError
    session = database.get_db_session()
    try:
        yield session

        if commit:
            session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


class MissingDatabaseError(Exception):
    """Database does not exist"""
    pass
