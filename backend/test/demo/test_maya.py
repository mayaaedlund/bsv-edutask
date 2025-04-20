import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController

pytestmark = pytest.mark.unit 


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

# Testcase 3: Two user with same email found
def test_valid_email_multiple_users(controller, userOne, userTwo, valid_email, capsys):
    """ 
    Should return the first user
    Print a warning message 
    """
    user_controller = controller([userOne, userTwo]) # Database with two users
    result = user_controller.get_user_by_email(valid_email)
    
    # Check if first user is returned
    assert result == userOne

    # Check if watning message is printed. 
    captured = capsys.readouterr()
    assert f"more than one user found with mail {valid_email}" in captured.out