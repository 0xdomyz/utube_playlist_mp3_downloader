# set up pytest fixtures
from pathlib import Path
import time
import shutil

here = Path(__file__).resolve().parent

import pytest

# tiredown and setup functions


@pytest.fixture(scope="session", autouse=True)
def setup():
    try:
        shutil.rmtree(here / "mp3_dir")
    except Exception:
        pass

    try:
        (here / "test.log").unlink()
    except Exception:
        pass
    yield


@pytest.fixture(autouse=True)
def add_cooldown():
    """Add cooldown between tests to avoid rate limiting"""
    yield
    time.sleep(0.5)
