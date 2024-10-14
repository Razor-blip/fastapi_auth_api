from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from app import database, crud, schemas, auth, database
from app.utils import get_password_hash
from app.database import get_db

load_dotenv()
app = FastAPI()

# User registration endpoint
@app.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    return crud.create_user(db=db, user=user, hashed_password=hashed_password)

# User login endpoint
@app.post("/login")
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Get current user based on JWT token
@app.get("/me", response_model=schemas.User)
def read_users_me(current_user: database.User = Depends(auth.get_current_user)):
    return current_user
