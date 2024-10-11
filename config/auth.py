import os
from datetime import timedelta, datetime

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from config.database import get_db
from models.customers import Customer

SECRET_KEY = os.getenv("PRIVATE_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 60

if not SECRET_KEY or not ALGORITHM:
    raise RuntimeError("SECRET_KEY or ALGORITHM is not set in environment variables")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_access_token(email: str, customer_id: int, role_id: int, expires_delta: timedelta):
    to_encode = {"sub": email, "id": customer_id, "role": role_id}
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



async def get_current_customer(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        customer_id: int = payload.get("id")

        if customer_id is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")

        customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()

        if customer is None:
            raise HTTPException(status_code=401, detail="Customer not found")

        return customer

    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    except Exception as e:
        print(f"Unexpected error in get_current_customer: {e}")
        raise HTTPException(status_code=500, detail='Internal Server Error')




def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(plain_password: str) -> str:
    return pwd_context.hash(plain_password)