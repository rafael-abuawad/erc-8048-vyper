import boa

ERC8048_INTERFACE_ID = bytes.fromhex("df670be1")


def test_deploy_free_mint_owner_and_balance(erc8048_mock_contract, alice):
    erc8048_mock_contract.freeMint(alice, 1)
    assert erc8048_mock_contract.ownerOf(0) == alice
    assert erc8048_mock_contract.balanceOf(alice) == 1


def test_setkeys_setmetadata_metadata_roundtrip(erc8048_mock_contract, alice):
    erc8048_mock_contract.freeMint(alice, 1)
    keys = ["name"]
    value = b"mock-token"
    erc8048_mock_contract.setKeys(keys)
    erc8048_mock_contract.setMetadata(0, [value])

    assert erc8048_mock_contract.metadata(0, "name") == value


def test_supportsinterface_includes_erc8048(erc8048_mock_contract):
    assert erc8048_mock_contract.supportsInterface(ERC8048_INTERFACE_ID)


def test_setmetadata_before_setkeys_reverts(erc8048_mock_contract, alice):
    erc8048_mock_contract.freeMint(alice, 1)
    with boa.reverts("erc8048: no keys set for token"):
        erc8048_mock_contract.setMetadata(0, [b"x"])


def test_setmetadata_length_mismatch_reverts(erc8048_mock_contract, alice):
    erc8048_mock_contract.freeMint(alice, 1)
    erc8048_mock_contract.setKeys(["only"])
    with boa.reverts("erc8048: must be the same length"):
        erc8048_mock_contract.setMetadata(0, [b"a", b"b"])
