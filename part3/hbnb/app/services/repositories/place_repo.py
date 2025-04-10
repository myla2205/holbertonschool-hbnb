#!/usr/bin/python3

from hbnb.app.models.place import Place
from hbnb.app.persistence.repository import SQLAlchemyRepository

class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)