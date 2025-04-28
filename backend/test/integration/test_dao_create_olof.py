import pytest
from pymongo import MongoClient
from pymongo.errors import WriteError, DuplicateKeyError
from unittest.mock import MagicMock
from src.util.dao import DAO
from bson import ObjectId
from datetime import datetime

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
        "title": "A valid task",
        "description": "A task description",
        "startdate": datetime.utcnow(),
        "duedate": datetime.utcnow(),
        "requires": [ObjectId(), ObjectId()],
        "categories": ["cat1", "cat2"],
        "todos": [ObjectId(), ObjectId()],
        "video": ObjectId()
    }

@pytest.fixture
def valid_todo():
    return {
        "description": "A todo description of a valid todo",
        "done": False
    }

# Test case 1
def test_create_valid_task(dao, valid_task):
    """ Should create and return a valid task """
    sut = dao(collection_name="task")
    res = sut.create(valid_task)
    assert res["title"] == valid_task["title"]

# Test case 2 (part 1-2)
@pytest.mark.parametrize(
    "invalid_task",
    [
        { "title": "Description is missing (required)" },
        { "title": "'description' has wrong bson type (string expected)", "description": 555 }
    ]
)
def test_create_invalid_tasks(dao, invalid_task):
    """ Should raise WriteError """
    sut = dao(collection_name="task")
    with pytest.raises(WriteError):
        sut.create(invalid_task)    # missing required field or wrong bson type

# Test case 2 (part 3)
def test_create_invalid_task_not_unique(dao, valid_task):
    """ Should raise DuplicateKeyError """
    sut = dao(collection_name="task")
    sut.create(valid_task)  # add a valid task
    with pytest.raises(DuplicateKeyError):
        sut.create(valid_task)  # add a second task, with same title (not unique)

# Test case 3
def test_create_valid_todo(dao, valid_todo):
    """ Should create and return a valid todo """
    sut = dao(collection_name="todo")
    res = sut.create(valid_todo)
    assert res["description"] == valid_todo["description"]

# Test case 4 (part 1-2)
@pytest.mark.parametrize(
    "invalid_todo",
    [
        { "done": False }, # missing required field
        { "description": "'done' has wrong bson type (bool expected)", "done": "False" }
    ]
)
def test_create_invalid_todos(dao, invalid_todo):
    """ Should raise WriteError """
    sut = dao(collection_name="todo")
    with pytest.raises(WriteError):
        sut.create(invalid_todo)    # missing required field or wrong bson type

# Test case 4 (part 3)
def test_create_invalid_todo_not_unique(dao, valid_todo):
    """ Should raise DuplicateKeyError """
    sut = dao(collection_name="todo")
    sut.create(valid_todo)  # add a valid todo
    with pytest.raises(DuplicateKeyError):
        sut.create(valid_todo)  # add a second todo, with same description (not unique)

# Test case 9
def test_init_dao_invalid_collection_name(dao):
    """ Should handle invalid collection name gracefully, FileNotFoundError is not accepted """
    try:
        dao(collection_name="invalid_name")
    except FileNotFoundError:
        pytest.fail("FileNotFoundError is raised. A more graceful solution, eg. InvalidCollectionError, is required.")
