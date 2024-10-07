import logging
from datetime import timedelta
import pytest
import asyncio
import pytest_asyncio

from httpx import AsyncClient
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from testcontainers.core.waiting_utils import wait_for_logs
from testcontainers.postgres import PostgresContainer
from app.schemas.token_schema import TokenData

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from app.settings import settings
from app.auth.auth_deps import TokenHandler
from account_util import UserAccount

from app.dependencies.get_db import get_db
from app.run import server


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

    TestingAsyncSession = async_sessionmaker(
            bind=async_engine,
            autocommit=False,
            autoflush=True,
            expire_on_commit=False
        )

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Override get_db dependency to use the testing session
    async def override_get_db():
        async with TestingAsyncSession() as db:
            yield db

    server.dependency_overrides[get_db] = override_get_db

    yield async_engine

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)



@pytest.fixture(scope="function")
async def async_client(test_db):
    async with AsyncClient(app=server, base_url="http://127.0.0.1:8000") as client:
        yield client

user = UserAccount("test-user")


@pytest.fixture(scope="function")
async def second_user():
    return UserAccount("test-user-2")


@pytest.fixture
async def test_user(async_client):
    user_data = {
        'username': 'existing_user',
        'password': 'test_password',
        'email': 'existing@test.com'
    }
    return user_data


@pytest.fixture
async def register_test_user(async_client, test_user):
    data = {
        'username': test_user['username'],
        'password': test_user['password'],
        'email': test_user['email']
    }
    response = await async_client.post("/user/register", json=data)
    assert response.status_code == 200
    response_data = response.json()
    response_data['user-data']['user']['password'] = test_user['password']
    return response_data


@pytest.fixture
async def login_test_user(async_client, register_test_user):
    """Fixture to log in a registered user and return the token."""
    data = {
        'username': register_test_user['user-data']['user']['username'],
        'password': register_test_user['user-data']['user']['password']
    }
    response = await async_client.post("/user/login", json=data)
    assert response.status_code == 200
    response_data = response.json()
    token = response_data['data']['access_token']
    return token


@pytest.fixture
def expired_token(test_user):
    token_data = TokenData(
        username=test_user['username'],
        user_id='2'
    )
    return TokenHandler.create_access_token(
        token_data=token_data,
        expires_delta=timedelta(microseconds=1)
    )


@pytest.fixture
def admin_headers():
    bot_username = settings.GAME_BOT_USERNAME
    bot_id = settings.GAME_BOT_USER_ID
    token_data = TokenData(
        username=bot_username,
        user_id=str(bot_id)
    )

    auth_token = TokenHandler.create_access_token(
        token_data=token_data,
        expires_delta=timedelta(minutes=10)
    )
    return {"Authorization": f"Bearer {auth_token}"}
