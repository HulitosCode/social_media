from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.settings import Settings

from .models import User
from .schemas import UserCreate, UserUpdate

settings = Settings()

bcrypt_context = CryptContext(
    schemes=['bcrypt'], deprecated='auto'
)  # hasing password
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='v1/auth/token')


# check for existing user
async def existing_user(db: Session, username: str, email: str):
    return (
        db.query(User)
        .filter((User.username == username) | (User.email == email))
        .first()
    )


# create access token
async def create_access_token(username: str, id: int):
    encode = {'sub': username, 'id': id}
    expires = datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRE_MINS)
    encode.update({'exp': expires})
    return jwt.encode(
        encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )


# get current user from token
async def get_current_user(db: Session, token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get('sub')
        id: str = payload.get('id')
        expires: datetime = payload.get('exp')
        if datetime.fromtimestamp(expires) < datetime.utcnow():
            return None
        if username is None or id is None:
            return None
        return db.query(User).filter(User.id == id).first()
    except JWTError:
        return None


# get user from user id
async def get_user_from_user_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


async def create_user(db: Session, user: UserCreate):
    db_user = User(
        email=user.email.lower().strip(),
        username=user.username.lower().strip(),
        hashed_password=bcrypt_context.hash(user.password),
        dob=user.dob or None,
        gender=user.gender or None,
        bio=user.bio or None,
        location=user.location or None,
        profile_pic=user.profile_pic or None,
        name=user.name or None,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # Atualiza o db_user com dados do banco
    return db_user


# authentication
async def authenticate(db: Session, username: str, password: str):
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        print('no user')
        return None
    if not bcrypt_context.verify(password, db_user.hashed_password):
        return None
    return db_user


# update user
async def update_user(db: Session, db_user: User, user_update: UserUpdate):
    db_user.bio = user_update.bio or db_user.bio
    db_user.name = user_update.name or db_user.name
    db_user.dob = user_update.dob or db_user.dob
    db_user.gender = user_update.gender or db_user.gender
    db_user.location = user_update.location or db_user.location
    db_user.profile_pic = user_update.profile_pic or db_user.profile_pic

    db.commit()
