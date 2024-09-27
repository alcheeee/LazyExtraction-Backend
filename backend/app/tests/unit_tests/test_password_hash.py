import pytest
from app.auth.auth_deps import PasswordSecurity


class TestPasswordHash:

    async def test_hash_password(self):
        password = "testpassword"
        hashed = PasswordSecurity.hash_password(password)
        assert hashed != password
        assert len(hashed) > 0


    async def test_check_pass_hash(self):
        password = "testpassword"
        hashed = PasswordSecurity.hash_password(password)
        assert PasswordSecurity.check_pass_hash(password, hashed)
        assert not PasswordSecurity.check_pass_hash("wrongpassword", hashed)
