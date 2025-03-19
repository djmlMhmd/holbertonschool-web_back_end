#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initializ a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """save the user to the database. """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()

        return user

    def find_user_by(self, **kwargs) -> User:
        """ takes in arbitrary keyword arguments and returns
        the first row found in the users table as filtered
        by the method’s input arguments."""

        user = self._session.query(User).filter_by(**kwargs).first()

        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Locate the user to update, then will update the user’s
        attributes as passed in the method’s arguments then commit
        changes to the database."""

        user = self.find_user_by(id=user_id)
        if user is not None:
            for k, v in kwargs.items():
                if hasattr(user, k):
                    setattr(user, k, v)
                else:
                    raise ValueError
            self._session.commit()
