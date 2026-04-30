from moccasin.boa_tools import VyperContract
from mocks import erc8048_mock


def deploy() -> VyperContract:
    c: VyperContract = erc8048_mock.deploy()
    print("Deployed erc8048:", c.address)
    return c


def moccasin_main() -> VyperContract:
    return deploy()
