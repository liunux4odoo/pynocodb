
from dataclasses import dataclass
import pytest


@dataclass
class TestData:
    API_TOKEN = "YzDNLisEZQ4AuId1i9sodHbDC2eEJxadiAlRUHXu"
    USER_EMAIL = "test@host.com"
    USER_PASSWORD = "11111111"
    BASE = "test_base"
    TABLE = "test_table"


def pytest_configure():
    pytest.data = TestData()
