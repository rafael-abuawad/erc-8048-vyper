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


from src.interfaces import IERC8048
implements: IERC8048


from snekmate.auth import ownable as ow
initializes: ow


from src import erc8048
initializes: erc8048[ownable := ow]
exports: erc8048.__interface__


@deploy
@payable
def __init__():
    """
    @dev To omit the opcodes for checking the `msg.value`
         in the creation-time EVM bytecode, the constructor
         is declared as `payable`.
    @notice The `owner` role will be assigned to
            the `msg.sender`.
    """
    ow.__init__()
    erc8048.__init__()
