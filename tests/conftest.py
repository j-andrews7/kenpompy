import os
import pytest
from kenpompy.utils import login

@pytest.fixture(scope="session")
def browser():
	try:
		browser = login(os.environ["EMAIL"], os.environ["PASSWORD"])
	except Exception as e:
		pytest.exit(e)

	return browser