# pragma version ~=0.4.3
# pragma nonreentrancy off
"""
@title Modern and Gas-Efficient ERC-8048 Implementation
@custom:contract-name erc8048
@license GNU Affero General Public License v3.0 only
@author rafael-abuawad
@notice ERC-8048 onchain metadata extension
        (https://eips.ethereum.org/EIPS/eip-8048).
"""

from ethereum.ercs import IERC165
implements: IERC165


from interfaces import IERC8048
implements: IERC8048


# @dev ERC-8048 Keys: emitted when the keys are set.
event KeysSet:
    _keys: DynArray[String[64], 12]



_MAX_METADATA_KEYS: constant(uint256) = 12
_SUPPORTED_INTERFACES: constant(bytes4[2]) = [
    0x01FFC9A7,  # ERC-165
    0xdf670be1,  # ERC-8048
]


metadata: public(HashMap[uint256, HashMap[String[64], Bytes[256]]])
metadataKeys: public(DynArray[String[64], _MAX_METADATA_KEYS])


@external
def setMetadata(
    token_id: uint256, data: DynArray[Bytes[256], _MAX_METADATA_KEYS]
):
    """
    @dev Sets the metadata for a token.
         Does not check if the token exists.
    @param token_id The token ID to set the metadata for.
    @param data The data to set the metadata for.
    """
    self._set_metadata(token_id, data)


@external
def setKeys(keys: DynArray[String[64], _MAX_METADATA_KEYS]):
    """
    @dev Sets the keys for a token.
    @param keys The keys to set for the token.
    """
    self.metadataKeys = keys
    log KeysSet(_keys=keys)


@internal
def _set_metadata(
    token_id: uint256, data: DynArray[Bytes[256], _MAX_METADATA_KEYS]
):
    """
    @dev Sets the metadata for a token.
         Does not check if the token exists.
    @param token_id The token ID to set the metadata for.
    @param data The data to set the metadata for.
    """
    keys: DynArray[String[64], _MAX_METADATA_KEYS] = self.metadataKeys
    assert len(keys) != 0, "erc8048: no keys set for token"
    assert len(keys) == len(data), "erc8048: must be the same length"

    for i: uint256 in range(len(keys), bound=_MAX_METADATA_KEYS):
        key: String[64] = keys[i]
        metadata: Bytes[256] = data[i]
        self.metadata[token_id][key] = metadata
        log IERC8048.MetadataSet(
            _tokenId=token_id, _indexedKey=key, _key=key, _value=metadata
        )


@external
@view
def supportsInterface(interface_id: bytes4) -> bool:
    return interface_id in _SUPPORTED_INTERFACES
