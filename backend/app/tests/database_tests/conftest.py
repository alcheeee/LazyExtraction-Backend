import logging
import asyncio
import pytest
import pytest_asyncio
import factory
from faker import Faker

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from testcontainers.postgres import PostgresContainer
from testcontainers.core.waiting_utils import wait_for_logs

from app.models.models import User
from app.dependencies.get_db import get_db
from sqlmodel import SQLModel
from app.run import server
from fixtures import *


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope="session")
def postgres_container():
    logging.getLogger("testcontainers.core.waiting_utils").setLevel(logging.ERROR)
    container = PostgresContainer("postgres:16", driver="asyncpg").with_exposed_ports(5432)
    container.start()
    wait_for_logs(container, r".*database system is ready to accept connections.*")
    yield container
    container.stop()


@pytest.fixture(scope="function")
async def test_db(postgres_container):
    """Create a fresh PostgreSQL database for each test."""
    async_engine = create_async_engine(postgres_container.get_connection_url())

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield async_engine

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture(scope="function")
async def test_session(test_db):
    TestingAsyncSession = async_sessionmaker(
            bind=test_db,
            autocommit=False,
            autoflush=True,
            expire_on_commit=False
        )

    async with TestingAsyncSession() as session:
        yield session
