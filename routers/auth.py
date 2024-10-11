from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from schemas.auth import Token, CustomerRequest
from services.authentication_service import AuthenticationService, get_authen_service
from config.database import get_db

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(create_customer_request: CustomerRequest,
                   authen_service: AuthenticationService = Depends(get_authen_service),
                   db: Session = Depends(get_db)):
    try:
        response = authen_service.register_customer(db, create_customer_request)
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Unexpected error during registration: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/login", response_model=Token)
async def login(login_data: OAuth2PasswordRequestForm = Depends(),
                 authen_service: AuthenticationService = Depends(get_authen_service),
                 db: Session = Depends(get_db)):
    try:
        response = authen_service.authenticate_customer(db, login_data.username, login_data.password)
        if response is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return response
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
