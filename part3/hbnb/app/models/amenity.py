#!/usr/bin/python3

from hbnb.app.models.base_model import BaseModel
from hbnb.app import db

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        super().__init__()
        self.name = self._validate_name(name)

    def _validate_name(self, name):
        if len(name) == 0:
            raise ValueError("Name cannot be empty")
        if len(name) > 50:
            raise ValueError("Name must be less than 50 characters")
        return name