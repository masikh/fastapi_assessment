"""Token and user models"""

import re
from pydantic import BaseModel, field_validator


class Token(BaseModel):
    """Token model"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data model"""

    username: str or None = None


class User(BaseModel):
    """User model"""

    username: str
    email: str or None = None
    full_name: str or None = None
    disabled: bool or False = False
    is_admin: bool or False = False


class NewUser(User):
    """New user"""

    clear_password: str

    @field_validator("clear_password")
    def validate_password(cls, value):
        """Validator"""

        # Check if the password meets Google's typical requirements using a regular expression
        if not re.match(
            r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$!%^&*]).{8,}$", value
        ):
            raise ValueError(
                "Password must be 8 characters or more, "
                "with at least one uppercase letter, one lowercase letter, "
                "one digit, and one special character (@#$!%^&*)"
            )

        return value


class UserInDB(User):
    """User in db model"""

    hashed_password: str
