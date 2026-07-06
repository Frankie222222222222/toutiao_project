from fastapi import HTTPException
from utils.exception import http_exception_handler,integrity_error_handler,sqlalchemy_error_handler,general_exception_handler
from sqlalchemy.exc import IntegrityError,SQLAlchemyError

def register_exception_handles(app):
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(IntegrityError,integrity_error_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)
    app.add_exception_handler(Exception, general_exception_handler)