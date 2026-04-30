import boa

ERC165_INTERFACE_ID = bytes.fromhex("01FFC9A7")
ERC8048_INTERFACE_ID = bytes.fromhex("df670be1")
UNKNOWN_INTERFACE_ID = bytes.fromhex("FFFFFFFF")


def test_supports_interface_erc165(erc8048_contract):
    assert erc8048_contract.supportsInterface(ERC165_INTERFACE_ID)


def test_supports_interface_erc8048(erc8048_contract):
    assert erc8048_contract.supportsInterface(ERC8048_INTERFACE_ID)


def test_does_not_support_interface_unknown(erc8048_contract):
    assert not erc8048_contract.supportsInterface(UNKNOWN_INTERFACE_ID)


def test_non_owner_set_keys_reverts(bob, erc8048_contract):
    with boa.reverts("ownable: caller is not the owner"):
        with boa.env.prank(bob):
            erc8048_contract.setKeys(["key"])


def test_set_metadata_before_set_keys_reverts(alice, erc8048_contract):
    with boa.reverts("erc8048: no keys set for token"):
        with boa.env.prank(alice):
            erc8048_contract.setMetadata(1, [b"p"])


def test_set_metadata_length_mismatch_reverts(alice, erc8048_contract):
    with boa.env.prank(alice):
        erc8048_contract.setKeys(["single_key"])

        with boa.reverts("erc8048: must be the same length"):
            erc8048_contract.setMetadata(1, [b"a", b"b"])


def test_set_keys_setmetadata_metadata_roundtrip(alice, erc8048_contract):
    keys = ["title", "author"]
    data = [b"my-nft-title", b"alice"]
    with boa.env.prank(alice):
        erc8048_contract.setKeys(keys)

    with boa.env.prank(alice):
        erc8048_contract.setMetadata(42, data)

    assert erc8048_contract.metadata(42, "title") == b"my-nft-title"
    assert erc8048_contract.metadata(42, "author") == b"alice"


def test_set_keys_emits_keys_set_event(alice, erc8048_contract):
    with boa.env.prank(alice):
        keys = ["title", "author"]
        erc8048_contract.setKeys(keys)
        for i, key in enumerate(keys):
            assert erc8048_contract.metadataKeys(i) == key

        logs = erc8048_contract.get_logs()
        print(logs)


def test_metadata_unset_key_returns_empty(alice, erc8048_contract):
    with boa.env.prank(alice):
        erc8048_contract.setKeys(["known"])
        erc8048_contract.setMetadata(99, [b"only-one"])
    assert erc8048_contract.metadata(99, "known") == b"only-one"
    assert erc8048_contract.metadata(99, "missing_key") == b""


def test_metadata_overwrites_existing_key(alice, erc8048_contract):
    with boa.env.prank(alice):
        erc8048_contract.setKeys(["known"])
        erc8048_contract.setMetadata(99, [b"known-value"])

    assert erc8048_contract.metadata(99, "known") == b"known-value"

    with boa.env.prank(alice):
        erc8048_contract.setKeys(["new-key", "new-key-2"])
        erc8048_contract.setMetadata(99, [b"new-key-value", b"new-key-2-value"])

    assert erc8048_contract.metadata(99, "known") == b"known-value"
    assert erc8048_contract.metadata(99, "new-key") == b"new-key-value"
    assert erc8048_contract.metadata(99, "new-key-2") == b"new-key-2-value"


def test_metadata_uint256_value(alice, erc8048_contract):
    with boa.env.prank(alice):
        erc8048_contract.setKeys(["uint256-key"])
    key_value = (1000).to_bytes(32, "big")

    with boa.env.prank(alice):
        erc8048_contract.setMetadata(99, [key_value])
    assert erc8048_contract.metadata(99, "uint256-key") == key_value
