from core.exceptions import AppError, ConflictError, UnauthorizedError
from core.security import create_access_token, hash_password, verify_password
from repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, db):
        self.users = UserRepository(db)

    def register(self, email: str, username: str, password: str) -> dict:
        email = (email or "").strip().lower()
        username = (username or "").strip()
        if not email or not username or not password:
            raise AppError("please provide email, username, and password")
        if len(password) < 6:
            raise AppError("password must be at least 6 characters")
        if self.users.get_by_email(email):
            raise ConflictError("email is already registered")
        if self.users.get_by_username(username):
            raise ConflictError("username is already taken")
        user = self.users.create(
            email=email,
            username=username,
            hashed_password=hash_password(password),
        )
        token = create_access_token(user.id, user.username)
        return {"token": token, "user": user.to_dict()}

    def login(self, account: str, password: str) -> dict:
        account = account.strip()
        user = self.users.get_by_email(account.lower()) or self.users.get_by_username(account)
        if not user or not verify_password(user.hashed_password, password):
            raise UnauthorizedError("account or password is incorrect")
        token = create_access_token(user.id, user.username)
        return {"token": token, "user": user.to_dict()}
