""" Authorization routes """

from typing import Dict
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from models.user_models import Token, User, NewUser
from datetime import timedelta
from helpers.authentication import (
    authenticate_user,
    create_access_token,
    create_user,
    delete_user,
    get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

router = APIRouter()


class Authenticate:
    @staticmethod
    @router.post("/token", response_model=Token)
    async def get_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
        """
        ## Purpose:

        Create Bearer token for API authorization

        ## Notes on access-token:

         * An access token is valid for 120 minutes

        ## Usage:

        headers: {"Authorization": "Bearer token"}
        """
        user = authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "Bearer"}

    @staticmethod
    @router.post("/users/create", response_model=User)
    async def users_create(
        new_user: NewUser, current_user: User = Depends(get_current_active_user)
    ):
        """
        ## Purpose:

        Create a new user in the database

        ## Notes:

        Only admin users are allowed to create new users
        """

        created_user = create_user(new_user, current_user)
        return created_user

    @staticmethod
    @router.delete("/users/delete", response_model=Dict[str, str])
    async def users_delete(
        username: str, current_user: User = Depends(get_current_active_user)
    ):
        """
        ## Purpose:

        Remove a user from the database

        ## Notes:

        * Only admin users are allowed to remove a user from the database
        * It's not allowed to remove oneself
        """

        is_deleted = delete_user(username, current_user)

        if not is_deleted:
            return {"result": f"No such username in database: {username}"}
        return {"result": f"Deleted username: {username}"}
