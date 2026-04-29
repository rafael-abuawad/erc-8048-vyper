import boa
import pytest

from src import erc8084
from mocks import erc8048_mock


@pytest.fixture
def alice():
    addr = boa.env.generate_address(alias="alice")
    boa.env.set_balance(addr, 10**18)
    return addr


@pytest.fixture
def erc8084_contract():
    return erc8084.deploy()


@pytest.fixture
def erc8048_mock_contract():
    return erc8048_mock.deploy(
        "TestNFT",
        "TNFT",
        "https://example.com/metadata/",
        "TestNFT",
        "1",
    )
