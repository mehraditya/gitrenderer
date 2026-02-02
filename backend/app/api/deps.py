from app.services.storage import LocalStorage 
from app.core.db import SessionLocal 


def get_Storage()-> LocalStorage:
    return LocalStorage()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()