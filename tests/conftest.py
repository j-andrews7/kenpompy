import os
import pytest
from kenpompy.utils import login

@pytest.fixture(scope="session")
def browser():
    bowser = login(os.environ["EMAIL"], os.environ["PASSWORD"])
    return bowser