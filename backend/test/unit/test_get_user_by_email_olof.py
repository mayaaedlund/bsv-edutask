import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController

pytestmark = pytest.mark.unit

class DatabaseException(Exception):
    """ Custom simulated database exception """
    pass

@pytest.fixture
def valid_email():
    """ Valid email format: <local-part>@<domain>.<host> """
    return "test.testsson@example.com"

@pytest.fixture
def user1(valid_email):
    return {"id": 1, "email": valid_email}

@pytest.fixture
def user2(valid_email):
    return {"id": 2, "email": valid_email}

@pytest.fixture
def error_message(valid_email):
    return f"Error: more than one user found with mail {valid_email}\n"

def test_get_user_by_email_1(valid_email):
    mock_DAO = MagicMock()
    mock_DAO.find.return_value = []   # no matching user
    sut = UserController(mock_DAO)

    res = sut.get_user_by_email(valid_email)

    assert res == None

def test_get_user_by_email_2(user1, valid_email):
    mock_DAO = MagicMock()
    mock_DAO.find.return_value = [user1]   # 1 matching user
    sut = UserController(mock_DAO)

    res = sut.get_user_by_email(valid_email)

    assert res == user1

def test_get_user_by_email_3(user1, user2, valid_email, error_message, capfd):
    mock_DAO = MagicMock()
    mock_DAO.find.return_value = [user1, user2]   # 2 matching users
    sut = UserController(mock_DAO)

    res = sut.get_user_by_email(valid_email)
    std_out, _ = capfd.readouterr()

    assert res == user1
    assert std_out == error_message

def test_get_user_by_email_4(valid_email):
    mock_DAO = MagicMock()
    mock_DAO.find.side_effect = DatabaseException("Error occured in database")  # db error
    sut = UserController(mock_DAO)

    with pytest.raises(DatabaseException):
        sut.get_user_by_email(valid_email)

@pytest.mark.parametrize("invalid_email", ["@no.local-part.com", "no.at-symbol.com", "double@@symbols.com", "no@.domain", "no@host"])
def test_get_user_by_email_5(invalid_email):
    """ valid email format: <local-part>@<domain>.<host> """
    mock_DAO = MagicMock()  # mocking just to make sure rest of function logic doesnt throw other errors
    sut = UserController(mock_DAO)

    with pytest.raises(ValueError):
        sut.get_user_by_email(invalid_email)    # 5 invalid emails
