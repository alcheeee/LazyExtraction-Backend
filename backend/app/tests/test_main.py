import pytest


from .all_tests.test_routes import (
    TestRoutes
)

from .all_tests.test_auth import (
    TestRegister,
    TestLogin,
    TestAuthTokens
)

from .all_tests.test_crews import (
    TestCrews
)

from .all_tests.test_raids import (
    TestRaids
)

from .all_tests.test_item_related import (
    TestInventory
)


from .all_tests.test_market import (
    TestMarket
)