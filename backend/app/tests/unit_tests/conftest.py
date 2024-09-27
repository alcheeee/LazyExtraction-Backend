import pytest_asyncio
import asyncio
import pytest
from app.tests.unit_tests.fixtures import *


@pytest.fixture
def anyio_backend():
    return 'asyncio'
