from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..auth.service import get_current_user
from ..database import get_db
from .schemas import FollowersList, FollowingList, Profile
from .service import (
    existing_user,
    follow_svc,
    get_followers_svc,
    get_following_svc,
    unfollow_svc,
)

router = APIRouter(prefix='/profile', tags=['profile'])


@router.get('/user/{username}', response_model=Profile)
async def profile(username: str, db: Session = Depends(get_db)):
    db_user = await existing_user(db, username, '')
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Invalid username'
        )

    return db_user


@router.post('/follow/{username}', status_code=status.HTTP_204_NO_CONTENT)
async def follow(username: str, token: str, db: Session = Depends(get_db)):
    db_user = await get_current_user(db, token)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='invalid token'
        )

    res = await follow_svc(db, db_user.username, username)
    if res is False:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='could not follow'
        )


@router.post('/unfollow/{username}', status_code=status.HTTP_204_NO_CONTENT)
async def unfollow(username: str, token: str, db: Session = Depends(get_db)):
    db_user = await get_current_user(db, token)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='invalid token'
        )

    res = await unfollow_svc(db, db_user.username, username)
    if res is False:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='could not follow'
        )


@router.get('/followers', response_model=FollowersList)
async def get_followers(token: str, db: Session = Depends(get_db)):
    current_user = await get_current_user(db, token)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid token'
        )
    return await get_followers_svc(db, current_user.id)


@router.get('/following', response_model=FollowingList)
async def get_following(token: str, db: Session = Depends(get_db)):
    current_user = await get_current_user(db, token)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid token'
        )
    return await get_following_svc(db, current_user.id)
