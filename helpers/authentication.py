"""Password verification helper methods"""

from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from models.user_models import User, NewUser, UserInDB, TokenData
from fastapi import Depends, HTTPException, status
from mock_data.mock_user_database import MockUserDatabase

# Authorization settings
SECRET_KEY = "4a725837375afeab021c937a2ba038e9b68d31fd9ebaaf07833e19ad13026a6b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

# password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")


def verify_password(plain_password, hashed_password):
    """Verify password"""

    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Get password hash for plain password"""

    return pwd_context.hash(password)


def get_user(username: str) -> UserInDB:
    """get user from database"""

    database = MockUserDatabase()
    user_data = database.get_user(username)
    if user_data:
        return UserInDB(**user_data)


def authenticate_user(username: str, password: str) -> UserInDB:
    """Authenticate user"""

    user = get_user(username)
    if user and verify_password(password, user.hashed_password):
        return user


def create_access_token(data: dict, expires_delta: timedelta or None = None):
    """Create access token"""

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=30)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current user"""

    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception

        token_data = TokenData(username=username)
    except JWTError as exc:
        raise credential_exception from exc

    user = get_user(username=token_data.username)
    if user is None:
        raise credential_exception

    return user


async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    """Check if user is active"""

    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return current_user


def create_user(new_user: NewUser, current_user: User) -> User:
    """Create new user

    NOTE: Password requirements are checked in the NewUser model
    """

    if current_user.is_admin is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized to make this request",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Setup database
    database = MockUserDatabase()

    # Check if user already exist
    existing_user = database.get_user(new_user.username)
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username taken",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # hash password
    hashed_password = get_password_hash(new_user.clear_password)

    # Create new user object
    user_in_db = UserInDB(
        hashed_password=hashed_password,
        username=new_user.username,
        full_name=new_user.full_name,
        email=new_user.email,
        is_admin=new_user.is_admin,
        disabled=new_user.disabled,
    )

    # Store user in database
    database.add_user(user_in_db.model_dump())

    # Return new user
    created_user = database.get_user(new_user.username)
    created_user.pop("hashed_password")

    return User(**created_user)


def delete_user(username: str, current_user: User) -> bool:
    """Delete user"""

    if current_user.is_admin is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized to make this request",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Setup database
    database = MockUserDatabase()

    # Check if we're not deleting our self
    if current_user.username == username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="It is forbidden to delete oneself.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Remove user from database
    result = database.delete_user(username)

    # Return result
    return result
