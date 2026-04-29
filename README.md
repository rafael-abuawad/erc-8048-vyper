<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="vyper-logo-dark.png">
    <img src="vyper-logo.png" width="140" alt="Vyper logo">
  </picture>
</p>

---

# ERC-8084 Vyper

Gas-efficient Vyper module for **[EIP-8084](https://eips.ethereum.org/EIPS/eip-8084)** onchain metadata extension: configurable string keys (up to 12), per-token `bytes` values, and `MetadataSet` events as defined by [`IERC8048`](src/interfaces/IERC8048.vyi). The implementation in this repository is **[`src/erc8084.vy`](src/erc8084.vy)**—a single module that implements [EIP-165](https://eips.ethereum.org/EIPS/eip-165) and IERC8048 (EIP-8048). Optional fields, access control, and token-existence checks are left to integrators; see NatSpec on the contract.

The interface file uses the **IERC8048** / **EIP-8048** naming from the ERC family; the primary Vyper module filename and header follow **ERC-8084** / **EIP-8084**.

## Contracts

| Path | Description |
|------|-------------|
| [`src/erc8084.vy`](src/erc8084.vy) | ERC-8084 implementation: IERC165, IERC8048, `setKeys` / `setMetadata`, `KeysSet`, public `metadata` / `metadataKeys`; interface IDs in `_SUPPORTED_INTERFACES` |
| [`src/interfaces/IERC8048.vyi`](src/interfaces/IERC8048.vyi) | IERC8048 interface (`metadata`, `MetadataSet` event) |
| [`mocks/erc8048_mock.vy`](mocks/erc8048_mock.vy) | Mock that composes ERC-721 (snekmate) with the extension; used by [`script/deploy.py`](script/deploy.py) and [`tests/test_erc8048_mock.py`](tests/test_erc8048_mock.py) |
| [`moccasin.toml`](moccasin.toml) | Moccasin project config (snekmate dependency, networks) |

**Standards:** [EIP-165](https://eips.ethereum.org/EIPS/eip-165) via `IERC165`; IERC8048 / EIP-8048 as declared in `_SUPPORTED_INTERFACES` in [`src/erc8084.vy`](src/erc8084.vy) (`0x01ffc9a7`, `0xdf670be1`).

## Dependencies

- [Vyper](https://docs.vyperlang.org/) `~=0.4.3` (see contract pragmas)
- [Moccasin](https://github.com/Cyfrin/moccasin) (build, test, deploy)
- Python `>=3.11`; [pyproject.toml](pyproject.toml) pins `moccasin`, `mamushi`, `ruff`
- [snekmate](https://github.com/pcaversaccio/snekmate) (`mox install` / [moccasin.toml](moccasin.toml)—used by the mock, not by the bare [`erc8084`](src/erc8084.vy) module)
- [Titanoboa](https://github.com/vyperlang/titanoboa) (`boa`, test backend via Moccasin)

## Install

```bash
uv tool install moccasin
mox install
```

## Build

```bash
mox compile
```

Artifacts are written under `out/`.

## Test

```bash
mox test
```

[`tests/conftest.py`](tests/conftest.py) deploys the bare [`src/erc8084.vy`](src/erc8084.vy) module for [`tests/test_erc8084.py`](tests/test_erc8084.py) and deploys [`mocks/erc8048_mock.vy`](mocks/erc8048_mock.vy) for [`tests/test_erc8048_mock.py`](tests/test_erc8048_mock.py).

## Deploy

```bash
mox run deploy
```

[`script/deploy.py`](script/deploy.py) deploys the mock with:

`erc8048_mock.deploy("Mock", "MOCK", "https://mock.com", "Mock", "1.0")`

For a live network, add or use a `[networks.*]` section in [`moccasin.toml`](moccasin.toml) and run:

```bash
mox run deploy --network <network-name> --account <keystore>
```

Production deployment of only [`src/erc8084.vy`](src/erc8084.vy) uses your own constructor / initializer pattern (the bare module has no snekmate dependency).

## EIP-165 interface identifiers

[`supportsInterface(bytes4)`](https://eips.ethereum.org/EIPS/eip-165) returns **true** for each interface identifier the contract implements. Per [EIP-165](https://eips.ethereum.org/EIPS/eip-165), an interface identifier is the bitwise XOR of the [function selectors](https://docs.soliditylang.org/en/latest/abi-spec.html#function-selector) of every **function** declared in that interface.

The **authoritative** values this contract advertises are the fixed `bytes4` entries in `_SUPPORTED_INTERFACES` in [`src/erc8084.vy`](src/erc8084.vy). They are **not** necessarily the output of a single [`cast sig`](https://book.getfoundry.sh/reference/cast/cast-sig) call.

### Verifying selectors (Foundry)

[`cast sig`](https://book.getfoundry.sh/reference/cast/cast-sig) prints each function’s selector. To cross-check an interface ID, XOR **all** selectors in that interface; the result must match the corresponding entry in `_SUPPORTED_INTERFACES` (XOR is associative and commutative, so order does not matter).

**IERC8048** (read API; see [`IERC8048.vyi`](src/interfaces/IERC8048.vyi)):

```bash
cast sig "metadata(uint256,string)"
```

**IERC165**:

```bash
cast sig "supportsInterface(bytes4)"
```

For IERC8048 with a single declared function, the interface identifier equals that function’s selector and must match `0xdf670be1`.

## Reference

- [EIP-8084](https://eips.ethereum.org/EIPS/eip-8084)
- [EIP-8048](https://eips.ethereum.org/EIPS/eip-8048) (IERC8048 naming)
- [EIP-165: Standard Interface Detection](https://eips.ethereum.org/EIPS/eip-165)
- [Moccasin documentation](https://cyfrin.github.io/moccasin)
- [Vyper documentation](https://vyper.readthedocs.io/)

---

*This is an unaudited reference implementation for educational and development purposes. It is not production-ready software. Use at your own risk. The authors accept no liability for losses or damages arising from its use or deployment. Contract headers license the code under GNU Affero General Public License v3.0 only.*
