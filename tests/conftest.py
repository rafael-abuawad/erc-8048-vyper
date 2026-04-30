import boa
import pytest
from mocks import erc8048_mock


@pytest.fixture
def alice():
    addr = boa.env.generate_address(alias="alice")
    boa.env.set_balance(addr, 10**18)
    return addr


@pytest.fixture
def bob():
    addr = boa.env.generate_address(alias="bob")
    boa.env.set_balance(addr, 10**18)
    return addr


@pytest.fixture
def erc8048_contract(alice):
    with boa.env.prank(alice):
        return erc8048_mock.deploy()
