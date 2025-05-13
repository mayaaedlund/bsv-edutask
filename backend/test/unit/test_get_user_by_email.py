# Authors: Maya Edlund and Olof Jönsson

import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController

pytestmark = pytest.mark.unit


class DatabaseException(Exception):
    """ Custom simulated database exception """
    pass


# Fixtures 

@pytest.fixture
def valid_email():
    """ Valid email should contain one '@' and a '.' in the domain. """
    return "test@test.com"

@pytest.fixture
def userOne(valid_email):
    """ Returns a user """
    return {"email": valid_email, "name": "Single User"}

@pytest.fixture
def userTwo(valid_email):
    """ Returns a different user with same email as userOne """
    return {"email": valid_email, "name": "Second User"}

@pytest.fixture
def controller():
    """ Creates a UserController object with mocked DAO. """
    def _controller(return_value):
        mock_dao = MagicMock()
        mock_dao.find.return_value = return_value
        return UserController(dao=mock_dao)
    return _controller


# Test cases

# Testcase 1: No user found
# Test fails, code tries to return a user from an empty list!
def test_valid_email_no_user(controller, valid_email):
    """ 
    Testcase when no user is found 
    Should return None
    """
    user_controller = controller([]) # Empty database
    result = user_controller.get_user_by_email(valid_email)
    assert result is None

# Testcase 2: one user found
def test_valid_email_one_user(controller, userOne, valid_email):
    """ 
    Testcase when excactly one user is found 
    Should return user
    """
    user_controller = controller([userOne]) # Database with one user. 
    result = user_controller.get_user_by_email(valid_email)
    assert result == userOne

# Testcase 3a: Two user with same email found - should return user-
def test_valid_email_multiple_users_returns_first(controller, userOne, userTwo, valid_email):
    """Should return the first user if multiple users have the same email"""
    user_controller = controller([userOne, userTwo])
    result = user_controller.get_user_by_email(valid_email)
    assert result == userOne


# Testcase 3b: Two users with same email - Should print a warning.
def test_valid_email_multiple_users_prints_warning(controller, userOne, userTwo, valid_email, capsys):
    """Should print a warning if multiple users are found with the same email"""
    user_controller = controller([userOne, userTwo])
    user_controller.get_user_by_email(valid_email)
    captured = capsys.readouterr()
    assert f"more than one user found with mail {valid_email}" in captured.out


# Testcase 4: Database fails (raises DatabaseException)
def test_valid_email_db_error(valid_email):
    """ Should raise Exception when database fails """
    mock_DAO = MagicMock()
    mock_DAO.find.side_effect = DatabaseException("Error occured in database")  # db error
    sut = UserController(dao=mock_DAO)

    with pytest.raises(DatabaseException):
        sut.get_user_by_email(valid_email)

# Testcase 5: Invalid emails
# Four invalid email formats makes the tests fail, due to a regex that is too simple
@pytest.mark.parametrize("invalid_email", ["@no.local-part.com", "no.at-symbol.com", "double@@symbols.com", "no@.domain", "no@host"])
def test_invalid_emails(controller, invalid_email):
    """
    Should raise ValueError when email is invalid (all 5 versions)
    valid email format: <local-part>@<domain>.<host>
    """
    sut = controller("A return value") # mocking just to make sure rest of function logic doesnt throw other exceptions

    with pytest.raises(ValueError):
        sut.get_user_by_email(invalid_email)    # 5 invalid emails
