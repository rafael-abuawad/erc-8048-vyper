# pragma version ~=0.4.3
# pragma nonreentrancy off
"""
@title `erc8048` Module Reference Implementation
@custom:contract-name erc8048_mock
@license GNU Affero General Public License v3.0 only
@author rafael-abuawad
"""


from ethereum.ercs import IERC165
implements: IERC165


from ethereum.ercs import IERC721
implements: IERC721


from snekmate.tokens.interfaces import IERC721Metadata
implements: IERC721Metadata


from snekmate.tokens.interfaces import IERC721Enumerable
implements: IERC721Enumerable


from snekmate.tokens.interfaces import IERC721Permit
implements: IERC721Permit


from snekmate.tokens.interfaces import IERC4906
implements: IERC4906


from snekmate.utils.interfaces import IERC5267
implements: IERC5267


from snekmate.auth import ownable as ow
initializes: ow


from snekmate.tokens import erc721
initializes: erc721[ownable := ow]
exports: (
    erc721.name,
    erc721.symbol,
    erc721.transferFrom,
    erc721.safeTransferFrom,
    erc721.approve,
    erc721.setApprovalForAll,
    erc721.getApproved,
    erc721.isApprovedForAll,
    erc721.ownerOf,
    erc721.balanceOf,
    erc721.tokenOfOwnerByIndex,
    erc721.tokenByIndex,
    erc721.totalSupply,
    erc721.tokenURI,
    erc721.DOMAIN_SEPARATOR,
    erc721.nonces,
    erc721.permit,
    erc721.eip712Domain
)


from ..src.interfaces import IERC8048
implements: IERC8048


from ..src import erc8048
initializes: erc8048
exports: (
    erc8048.metadata,
    erc8048.setMetadata,
    erc8048.setKeys,
)


_SUPPORTED_INTERFACES: constant(bytes4[8]) = [
    erc721._SUPPORTED_INTERFACES[0],
    erc721._SUPPORTED_INTERFACES[1],
    erc721._SUPPORTED_INTERFACES[2],
    erc721._SUPPORTED_INTERFACES[3],
    erc721._SUPPORTED_INTERFACES[4],
    erc721._SUPPORTED_INTERFACES[5],
    erc8048._SUPPORTED_INTERFACES[0],
    erc8048._SUPPORTED_INTERFACES[1],
]


@deploy
@payable
def __init__(
    name_: String[25], symbol_: String[5], base_uri_: String[80], name_eip712_: String[50], version_eip712_: String[20]
):
    """
    @dev To omit the opcodes for checking the `msg.value`
         in the creation-time EVM bytecode, the constructor
         is declared as `payable`.
    @notice The `owner` role will be assigned to
            the `msg.sender`.
    @param name_ The maximum 25-character user-readable string
           name of the token collection.
    @param symbol_ The maximum 5-character user-readable string
           symbol of the token collection.
    @param base_uri_ The maximum 80-character user-readable
           string base URI for computing `tokenURI`.
    @param name_eip712_ The maximum 50-character user-readable
           string name of the signing domain, i.e. the name
           of the dApp or protocol.
    @param version_eip712_ The maximum 20-character current
           main version of the signing domain. Signatures
           from different versions are not compatible.
    """
    ow.__init__()
    erc721.__init__(name_, symbol_, base_uri_, name_eip712_, version_eip712_)


@external
def freeMint(owner: address, amount: uint256):
    """
    @dev Creates `amount` tokens and assigns them to
         `owner`, increasing the total supply.
    @notice Note that each `token_id` must not exist
            and `owner` cannot be the zero address.
    @param owner The 20-byte owner address.
    @param amount The 32-byte token amount to be created.
    """
    for _: uint256 in range(amount, bound=64):
        token_id: uint256 = erc721._counter
        erc721._counter = token_id + 1
        erc721._mint(owner, token_id)
    

@external
@view
def supportsInterface(interface_id: bytes4) -> bool:
    return interface_id in _SUPPORTED_INTERFACES