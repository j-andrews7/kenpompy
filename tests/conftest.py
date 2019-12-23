import os
import pytest
from kenpompy.utils import login

def pytest_generate_tests(metafunc):
    if "browser" in metafunc.fixturenames:
        browser = login(os.environ["EMAIL"], os.environ["PASSWORD"])
        metafunc.parametrize("browser", browser)