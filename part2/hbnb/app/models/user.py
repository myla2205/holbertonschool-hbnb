#!/usr/bin/python3

from datetime import datetime
from hbnb.app.models.base_model import BaseModel
import re

# This variable is used to validate the email format
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = self._validate_first_name(first_name)
        self.last_name = self._validate_last_name(last_name)
        self.email = self._validate_email(email)
        self.is_admin = is_admin
        self.places = []

    def _validate_email(self, email):
        if not re.fullmatch(regex, email):
            raise ValueError("Invalid email format")
        return email

    def _validate_first_name(self, first_name):
        if len(first_name) > 50:
            raise ValueError("First name must be less than 50 characters")
        if len(first_name) == 0:
            raise ValueError("First name cannot be empty")
        return first_name
    def _validate_last_name(self, last_name):
        if len(last_name) > 50:
            raise ValueError("Last name must be less than 50 characters")
        if len(last_name) == 0:
            raise ValueError("Last name cannot be empty")
        return last_name