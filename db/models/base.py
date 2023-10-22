from typing import Any
from datetime import date, datetime
from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class Base:
    id: Any

    def as_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for key, value in data.items():
            if isinstance(value, datetime) or isinstance(value, date):
                data[key] = str(value)
        return data
