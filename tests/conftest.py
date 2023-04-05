# set up pytest fixtures
from pathlib import Path

here = Path(__file__).resolve().parent

import pytest

# tiredown and setup functions


@pytest.fixture(scope="session", autouse=True)
def setup():
    try:
        (here / "test.log").unlink()
    except Exception:
        pass
    yield
