import os
import pytest
from kenpompy.utils import login

@pytest.fixture(scope="session")
def get_browser():
    browser = login(os.environ["EMAIL"], os.environ["PASSWORD"])
    return browser