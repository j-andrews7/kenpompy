import os
import pytest
from kenpompy.utils import login


def test_login():

	with pytest.raises(Exception):
		browser = login("i am a fake email", "my password is password")
