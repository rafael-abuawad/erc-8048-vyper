import boa

ERC165_INTERFACE_ID = bytes.fromhex("01FFC9A7")
ERC8048_INTERFACE_ID = bytes.fromhex("df670be1")
UNKNOWN_INTERFACE_ID = bytes.fromhex("FFFFFFFF")


def test_supportsinterface_erc165_and_erc8048_true(erc8048_contract):
    assert erc8048_contract.supportsInterface(ERC165_INTERFACE_ID)
    assert erc8048_contract.supportsInterface(ERC8048_INTERFACE_ID)
    assert not erc8048_contract.supportsInterface(UNKNOWN_INTERFACE_ID)


def test_setmetadata_before_setkeys_reverts(erc8048_contract):
    with boa.reverts("erc8048: no keys set for token"):
        erc8048_contract.setMetadata(1, [b"p"])


def test_setmetadata_length_mismatch_reverts(erc8048_contract):
    erc8048_contract.setKeys(["single_key"])
    with boa.reverts("erc8048: must be the same length"):
        erc8048_contract.setMetadata(1, [b"a", b"b"])


def test_setkeys_setmetadata_metadata_roundtrip(erc8048_contract):
    keys = ["title", "author"]
    data = [b"my-nft-title", b"alice"]
    erc8048_contract.setKeys(keys)

    erc8048_contract.setMetadata(42, data)

    assert erc8048_contract.metadata(42, "title") == b"my-nft-title"
    assert erc8048_contract.metadata(42, "author") == b"alice"


def test_metadata_unset_key_returns_empty(erc8048_contract):
    erc8048_contract.setKeys(["known"])
    erc8048_contract.setMetadata(99, [b"only-one"])
    assert erc8048_contract.metadata(99, "known") == b"only-one"
    assert erc8048_contract.metadata(99, "missing_key") == b""
