from typing import TypeVar, Generic
from pydantic import BaseModel

T = TypeVar('T')

class BaseResponse(BaseModel, Generic[T]):
    message: str
    status: str
    data: T
