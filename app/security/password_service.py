from passlib.context import CryptContext

from app.core.config import settings


class PasswordService:
    password_context = CryptContext(schemes=settings.CRYPT_CONTEXT, deprecated="auto")

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.password_context.verify(password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.password_context.hash(password)


password_service = PasswordService()
