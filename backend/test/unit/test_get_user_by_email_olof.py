import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController

pytestmark = pytest.mark.unit

class DatabaseException(Exception):
    """ Custom simulated database exception """
    pass

# Constants
VALID_EMAIL = "test.testsson@example.com"   # valid email format: <local-part>@<domain>.<host>
USER1 = {"id": 1, "email": VALID_EMAIL}
USER2 = {"id": 2, "email": VALID_EMAIL}
ERROR_MSG = f"Error: more than one user found with mail {VALID_EMAIL}\n"


@pytest.mark.parametrize(
    "users, email, expected",
    [
        ([], VALID_EMAIL, None),        # test case 1
        ([USER1], VALID_EMAIL, USER1),  # test case 2
    ]
)
def test_get_user_by_email_1_2(users, email, expected):
    mock_DAO = MagicMock()
    mock_DAO.find.return_value = users
    sut = UserController(mock_DAO)

    res = sut.get_user_by_email(email)

    assert res == expected


def test_get_user_by_email_3(capfd):
    mock_DAO = MagicMock()
    mock_DAO.find.return_value = [USER1, USER2]
    sut = UserController(mock_DAO)

    res = sut.get_user_by_email(VALID_EMAIL)
    std_out, _ = capfd.readouterr()

    assert res == USER1
    assert std_out == ERROR_MSG


def test_get_user_by_email_4():
    mock_DAO = MagicMock()
    mock_DAO.find.side_effect = DatabaseException("Error occured in database")
    sut = UserController(mock_DAO)

    with pytest.raises(DatabaseException):
        sut.get_user_by_email(VALID_EMAIL)


@pytest.mark.parametrize("invalid_email", ["@no.local-part.com", "no.at-symbol.com", "double@@symbols.com", "no@.domain", "no@host"])
def test_get_user_by_email_5(invalid_email):
    """ valid email format: <local-part>@<domain>.<host> """
    mock_DAO = MagicMock()  # mocking just to make sure rest of function logic doesnt throw other errors
    sut = UserController(mock_DAO)

    with pytest.raises(ValueError):
        sut.get_user_by_email(invalid_email)
