from starlette import status
from user_microservice.infra.postgres.tables import BaseDBModel
from typing import Type

class BaseError(Exception):
    def __init__(
            self,
            message='Произошла неизвестная ошибка.',
            status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    ) -> None:
        self.status_code = status_code
        self.message = message
    
    def __str__(self) -> str:
        return self.message

class InvalidCredentialsError(BaseError):
    def __init__(self,
                 message: str = 'Неверный логин или пароль.',
                 status_code = status.HTTP_401_UNAUTHORIZED):
        super().__init__(message, status_code)

class DataNotFoundError(BaseError):
    def __init__(self,
                 table: Type[BaseDBModel],
                 status_code = status.HTTP_404_NOT_FOUND):
        super().__init__(f'Объект в моделе {table} не найден', status_code)

class ConflictEmailError(BaseError):
    def __init__(self,
                message: str = "Пользователь с таким e-mail уже существует",
                status_code = status.HTTP_409_CONFLICT):
        super().__init__(message, status_code)

class ConflictPhoneError(BaseError):
    def __init__(self,
                message: str = "Пользователь с таким телефоном уже существует",
                status_code = status.HTTP_409_CONFLICT):
        super().__init__(message, status_code)
