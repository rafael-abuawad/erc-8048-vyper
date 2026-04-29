from moccasin.boa_tools import VyperContract
from mocks import erc8048_mock


def deploy() -> VyperContract:
    c: VyperContract = erc8048_mock.deploy(
        "Mock", "MOCK", "https://mock.com", "Mock", "1.0"
    )
    print("Deployed erc8084:", c.address)
    return c


def moccasin_main() -> VyperContract:
    return deploy()
