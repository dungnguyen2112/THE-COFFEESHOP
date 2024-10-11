from fastapi import HTTPException

from schemas.base_response import BaseResponse

ERROR_CODES = {
    # Authentication related errors (100000-100099)
    100001: 'Login failed!',
    100002: 'Credentials are not correct!',
    100003: 'Register failed!',
    100004: 'Unauthorized access!',
    100005: 'Token expired!',

    # Customer related errors (110000-110099)
    110001: 'Customer not found!',
    110002: 'Update customer failed!',
    110003: 'Delete customer failed!',
    110004: 'Password update failed!',

    # Product related errors (120000-120099)
    120001: 'Get all products failed!',
    120002: 'Product not found!',
    120003: 'Create product failed!',
    120004: 'Update product failed!',
    120005: 'Delete product failed!',

    # Order related errors (130000-130099)
    130001: 'Get all orders failed!',
    130002: 'Order not found!',
    130003: 'Create order failed!',
    130004: 'Update order failed!',
    130005: 'Delete order failed!',

    # Loyalty related errors (140000-140099)
    140001: 'Loyalty points retrieval failed!',
    140002: 'Update loyalty points failed!',

    # General errors (900000-900099)
    900001: 'Internal server error!',
    900002: 'Bad request!',
    900003: 'Resource not found!',
}

class StockQuantityError(HTTPException):
    def __init__(self, product_id: int, detail: str):
        super().__init__(status_code=400, detail=f"Product ID {product_id}: {detail}")

def raise_error(error_code: int) -> BaseResponse:
    return BaseResponse(
        message=ERROR_CODES.get(error_code, 'Unknown error occurred'),
        status='error',
    )