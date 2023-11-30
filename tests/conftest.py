import os
import pytest
from kenpompy.utils import login
import time
from random import randint

@pytest.fixture(scope="session")
def browser():
	try:
		browser = login(os.environ["EMAIL"], os.environ["PASSWORD"])
	except Exception as e:
		pytest.exit(e)

	return browser

@pytest.fixture(autouse=True)
def brakes():
    yield
    time.sleep(randint(2, 10))
