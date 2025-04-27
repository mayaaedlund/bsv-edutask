import pytest
from pymongo import MongoClient
from pymongo.errors import WriteError, DuplicateKeyError
from unittest.mock import MagicMock
from src.util.dao import DAO

pytestmark = pytest.mark.integration

@pytest.fixture(scope="module")
def mongo_test_url():
    return "mongodb://test:test@mongodb_test:27017"

@pytest.fixture(scope="module")
def mongo_client(mongo_test_url):
    return MongoClient(mongo_test_url)

@pytest.fixture
def set_MONGO_URL(mongo_test_url, monkeypatch):
    """ Patch env variable MONGO_URL """
    monkeypatch.setenv("MONGO_URL", mongo_test_url)

@pytest.fixture
def clean_up_database(mongo_client):
    yield
    mongo_client.drop_database("edutask")

@pytest.fixture
def dao(set_MONGO_URL, clean_up_database):
    """ DAO factory """
    def _dao(collection_name):
        dao = DAO(collection_name=collection_name)
        return dao
    return _dao


# Testcase 5
@pytest.fixture
def valid_user():
    return {
        "firstName": "FirstName",
        "lastName": "LastName",
        "email": "test@test.com",
        "tasks": []
    }

def test_create_valid_user(dao, valid_user):
    """Should create and return a valid user"""
    sut = dao(collection_name="user")
    res = sut.create(valid_user)
    
    assert res["firstName"] == valid_user["firstName"]
    assert res["lastName"] == valid_user["lastName"]
    assert res["email"] == valid_user["email"]
    assert res["tasks"] == valid_user["tasks"]
    assert "_id" in res

# Testcase 6
@pytest.mark.parametrize(
    "invalid_user",
    [
        {
            "lastName": "LastName",
            "email": "test@example.com",
            "tasks": []
        },  # Missing firstName
        {
            "firstName": "FirstName",
            "lastName": "LastName",
            "email": 11111,
            "tasks": []
        },  # Wrong type for email
    ]
)

# WriteError

def test_create_invalid_user(dao, invalid_user):
    """Should raise WriteError when user is invalid (missing fields or wrong type)"""
    sut = dao(collection_name="user")

    with pytest.raises(WriteError):
        sut.create(invalid_user)

# DublicateKeyError
def test_create_user_duplicate_email(dao, valid_user):
    """Should raise DublicateKeyError when creating user with duplicate email"""
    sut = dao(collection_name="user")
    sut.create(valid_user)  # Insert first user

    duplicate_user = {
        "firstName": "Duplicate",
        "lastName": "User",
        "email": valid_user["email"],  # Same email
        "tasks": []
    }

    with pytest.raises(DuplicateKeyError):
            sut.create(duplicate_user)
