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

@pytest.fixture
def valid_task():
    return {
        "title": "A title",
        "description": "A description"
    }

def test_create_task(dao, valid_task):
    """ Should create and return a valid task """
    sut = dao(collection_name="task")
    res = sut.create(valid_task)
    assert res["title"] == valid_task["title"]

@pytest.mark.parametrize(
    "invalid_task",
    [
        { "title": "Description is missing (required)" },
        { "title": "Description has wrong bson type (string expected)", "description": 555 }
    ]
)
def test_create_invalid_tasks(dao, invalid_task):
    """ Should raise WriteError """
    sut = dao(collection_name="task")
    with pytest.raises(WriteError):
        sut.create(invalid_task)

def test_create_invalid_task_not_unique(dao, valid_task):
    """ Should raise DuplicateKeyError """
    sut = dao(collection_name="task")
    sut.create(valid_task)  # add a valid task
    with pytest.raises(DuplicateKeyError):
        sut.create(valid_task)  # add a second task, with same title
