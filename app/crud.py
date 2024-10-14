from sqlalchemy.orm import Session
from app import database, schemas

def get_user_by_username(db: Session, username: str):
    return db.query(database.User).filter(database.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    db_user = database.User(username=user.username, full_name=user.full_name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
