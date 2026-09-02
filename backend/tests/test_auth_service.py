from types import SimpleNamespace

import pytest

from core.exceptions import AppError, ConflictError, UnauthorizedError
from services.auth_service import AuthService


@pytest.fixture
def auth_service(mocker):
    service = AuthService(db=None)
    service.users = mocker.MagicMock()
    return service


@pytest.fixture
def user():
    return SimpleNamespace(
        id=7,
        username="alice",
        hashed_password="stored-hash",
        to_dict=lambda: {"id": 7, "email": "alice@example.com", "username": "alice"},
    )


def test_register_normalizes_input_and_returns_token_and_user(auth_service, user, mocker):
    auth_service.users.get_by_email.return_value = None
    auth_service.users.get_by_username.return_value = None
    auth_service.users.create.return_value = user

    hash_password = mocker.patch("services.auth_service.hash_password", return_value="new-hash")
    create_access_token = mocker.patch("services.auth_service.create_access_token", return_value="token")

    result = auth_service.register("  ALICE@EXAMPLE.COM ", " alice ", "secret")

    hash_password.assert_called_once_with("secret")
    auth_service.users.create.assert_called_once_with(
        email="alice@example.com", username="alice", hashed_password="new-hash"
    )
    create_access_token.assert_called_once_with(7, "alice")
    assert result == {"token": "token", "user": user.to_dict()}


def test_register_rejects_missing_fields(auth_service):
    with pytest.raises(AppError, match="please provide email, username, and password"):
        auth_service.register("", "alice", "secret")

    auth_service.users.get_by_email.assert_not_called()


def test_register_rejects_short_password(auth_service):
    with pytest.raises(AppError, match="password must be at least 6 characters"):
        auth_service.register("alice@example.com", "alice", "short")

    auth_service.users.get_by_email.assert_not_called()


def test_register_rejects_duplicate_email(auth_service, user):
    auth_service.users.get_by_email.return_value = user

    with pytest.raises(ConflictError, match="email is already registered"):
        auth_service.register("alice@example.com", "alice", "secret")

    auth_service.users.get_by_username.assert_not_called()
    auth_service.users.create.assert_not_called()


def test_register_rejects_duplicate_username(auth_service, user):
    auth_service.users.get_by_email.return_value = None
    auth_service.users.get_by_username.return_value = user

    with pytest.raises(ConflictError, match="username is already taken"):
        auth_service.register("alice@example.com", "alice", "secret")

    auth_service.users.create.assert_not_called()


def test_login_with_email_normalizes_account_and_returns_user(auth_service, user, mocker):
    auth_service.users.get_by_email.return_value = user

    verify_password = mocker.patch("services.auth_service.verify_password", return_value=True)
    create_access_token = mocker.patch("services.auth_service.create_access_token", return_value="token")

    result = auth_service.login("  ALICE@EXAMPLE.COM ", "secret")

    auth_service.users.get_by_email.assert_called_once_with("alice@example.com")
    auth_service.users.get_by_username.assert_not_called()
    verify_password.assert_called_once_with("stored-hash", "secret")
    create_access_token.assert_called_once_with(7, "alice")
    assert result == {"token": "token", "user": user.to_dict()}


def test_login_falls_back_to_username(auth_service, user, mocker):
    auth_service.users.get_by_email.return_value = None
    auth_service.users.get_by_username.return_value = user

    mocker.patch("services.auth_service.verify_password", return_value=True)

    result = auth_service.login(" alice ", "secret")

    auth_service.users.get_by_email.assert_called_once_with("alice")
    auth_service.users.get_by_username.assert_called_once_with("alice")
    assert result["user"] == user.to_dict()


def test_login_rejects_unknown_account(auth_service, mocker):
    auth_service.users.get_by_email.return_value = None
    auth_service.users.get_by_username.return_value = None

    verify_password = mocker.patch("services.auth_service.verify_password")

    with pytest.raises(UnauthorizedError, match="account or password is incorrect"):
        auth_service.login("unknown", "secret")

    verify_password.assert_not_called()


def test_login_rejects_wrong_password(auth_service, user, mocker):
    auth_service.users.get_by_email.return_value = user

    mocker.patch("services.auth_service.verify_password", return_value=False)

    with pytest.raises(UnauthorizedError, match="account or password is incorrect"):
        auth_service.login("alice@example.com", "wrong")
