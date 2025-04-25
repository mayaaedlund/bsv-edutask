import pytest
from unittest.mock import MagicMock
from src.util.dao import DAO

pytestmark = pytest.mark.integration

@pytest.fixture
def sut():
    """  """
    pass

def test_create_video():
    """ MESSING AROUND """
    sut = DAO(collection_name="video")
    video = {"url": "www.test.se"}

    res = sut.create(data=video)

    print(res)
    assert res["url"] == "www.test.se"
