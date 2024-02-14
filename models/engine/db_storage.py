#!/usr/bin/python3
"""
Contains the class DBStorage
"""

from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models.amenity import Amenity
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

all_cls = {
    "State": State, "User": User,
    "Amenity": Amenity, "City": City,
    "Place": Place, "Review": Review
}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def new(self, obj):
        """new"""
        self.__session.add(obj)

    def all(self, cls=None):
        """all"""
        nd = {}
        for clss in all_cls:
            if cls is None or cls is all_cls[clss] or cls is clss:
                objs = self.__session.query(all_cls[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    nd[key] = obj
        return (nd)

    def delete(self, obj=None):
        """delete"""
        if obj is not None:
            self.__session.delete(obj)

    def save(self):
        """commit"""
        self.__session.commit()

    def close(self):
        """call"""
        self.__session.remove()

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sf = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sf)
        self.__session = Session

