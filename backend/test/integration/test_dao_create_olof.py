import pytest
from pymongo import MongoClient
from pymongo.errors import WriteError
from unittest.mock import MagicMock
from src.util.dao import DAO

pytestmark = pytest.mark.integration

@pytest.fixture
def mongo_test_url():
    return "mongodb://test:test@mongodb_test:27017"

@pytest.fixture
def mongo_client(mongo_test_url):
    return MongoClient(mongo_test_url)

@pytest.fixture
def set_MONGO_URL(mongo_test_url, monkeypatch):
    """ Patch env variable MONGO_URL """
    monkeypatch.setenv("MONGO_URL", mongo_test_url)

@pytest.fixture
def dao(set_MONGO_URL, mongo_client):
    """ DAO factory with db clean up """
    def _dao(collection_name):
        dao = DAO(collection_name=collection_name)
        return dao

    yield _dao

    mongo_client.drop_database("edutask")

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
    """ Should create and return a valid task """
    sut = dao(collection_name="task")
    with pytest.raises(WriteError):
        sut.create(invalid_task)
