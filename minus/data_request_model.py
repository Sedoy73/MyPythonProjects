from pydantic import BaseModel, validator, root_validator
from datetime import date
#from typing import Optional

class Staff (BaseModel)
    Firstname: str
    Lastname: str
    Address: str
    Birthdate: date
