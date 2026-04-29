<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="vyper-logo-dark.png">
    <img src="vyper-logo.png" width="140" alt="Vyper logo">
  </picture>
</p>

---

# ERC-8048 Vyper

**At a glance**

- [EIP-8048](https://eips.ethereum.org/EIPS/eip-8048) onchain metadata extension for token registries: configurable string keys (up to 12), per-token `bytes` values, and `MetadataSet` events as defined by [`IERC8048`](src/interfaces/IERC8048.vyi).
- Core implementation: **[`src/erc8048.vy`](src/erc8048.vy)** — [EIP-165](https://eips.ethereum.org/EIPS/eip-165) plus IERC8048.
- **[`mocks/erc8048_mock.vy`](mocks/erc8048_mock.vy)** composes ERC-721 (snekmate) with the extension for deploy scripts and tests.
- Optional fields, access control, and token-existence checks are left to integrators; see NatSpec on [`src/erc8048.vy`](src/erc8048.vy).

This repository is a gas-efficient Vyper module for that standard: one module that implements IERC8048 and advertises the correct interface IDs.

### Naming

The interface file follows **IERC8048** / **EIP-8048** naming from the ERC family; the primary Vyper module filename and header use **ERC-8048** / **EIP-8048**.

## Contracts

| Path | Description |
|------|-------------|
| [`src/erc8048.vy`](src/erc8048.vy) | Core ERC-8048 module: `IERC165`, `IERC8048`; interface IDs in `_SUPPORTED_INTERFACES` |
| [`src/interfaces/IERC8048.vyi`](src/interfaces/IERC8048.vyi) | IERC8048 interface (`metadata`, `MetadataSet` event) |
| [`mocks/erc8048_mock.vy`](mocks/erc8048_mock.vy) | Mock that composes ERC-721 (snekmate) with the extension; used by [`script/deploy.py`](script/deploy.py) and [`tests/test_erc8048_mock.py`](tests/test_erc8048_mock.py) |
| [`moccasin.toml`](moccasin.toml) | Moccasin project config (snekmate dependency, networks) |

API surface for [`src/erc8048.vy`](src/erc8048.vy):

- `setKeys`, `setMetadata`, `KeysSet`
- Public `metadata`, `metadataKeys`

**Standards:** [EIP-165](https://eips.ethereum.org/EIPS/eip-165) via `IERC165`; IERC8048 / EIP-8048 as declared in `_SUPPORTED_INTERFACES` in [`src/erc8048.vy`](src/erc8048.vy) (`0x01ffc9a7`, `0xdf670be1`).

## Dependencies

- [Vyper](https://docs.vyperlang.org/) `~=0.4.3` (see contract pragmas)
- [Moccasin](https://github.com/Cyfrin/moccasin) (build, test, deploy)
- Python `>=3.11`; [pyproject.toml](pyproject.toml) pins `moccasin`, `mamushi`, `ruff`
- [snekmate](https://github.com/pcaversaccio/snekmate) (`mox install` / [moccasin.toml](moccasin.toml)—used by the mock, not by the bare [`erc8048`](src/erc8048.vy) module)
- [Titanoboa](https://github.com/vyperlang/titanoboa) (`boa`, test backend via Moccasin)

## Quick start

### Install

```bash
uv tool install moccasin
mox install
```

### Build

```bash
mox compile
```

Artifacts are written under `out/`.

### Test

```bash
mox test
```

[`tests/conftest.py`](tests/conftest.py) deploys the bare [`src/erc8048.vy`](src/erc8048.vy) module for [`tests/test_erc8048.py`](tests/test_erc8048.py) and deploys [`mocks/erc8048_mock.vy`](mocks/erc8048_mock.vy) for [`tests/test_erc8048_mock.py`](tests/test_erc8048_mock.py).

## Deploy

```bash
mox run deploy
```

[`script/deploy.py`](script/deploy.py) deploys the mock with:

```python
erc8048_mock.deploy("Mock", "MOCK", "https://mock.com", "Mock", "1.0")
```

For a live network, add or use a `[networks.*]` section in [`moccasin.toml`](moccasin.toml) and run:

```bash
mox run deploy --network <network-name> --account <keystore>
```

Production deployment of only [`src/erc8048.vy`](src/erc8048.vy) uses your own constructor / initializer pattern (the bare module has no snekmate dependency).

## EIP-165 (interface IDs)

*Skip this section if you only need build, test, or deploy.*

[`supportsInterface(bytes4)`](https://eips.ethereum.org/EIPS/eip-165) returns **true** for each interface identifier the contract implements. Per [EIP-165](https://eips.ethereum.org/EIPS/eip-165), an interface identifier is the bitwise XOR of the [function selectors](https://docs.soliditylang.org/en/latest/abi-spec.html#function-selector) of every **function** declared in that interface.

The **authoritative** values this contract advertises are the fixed `bytes4` entries in `_SUPPORTED_INTERFACES` in [`src/erc8048.vy`](src/erc8048.vy). They are **not** necessarily the output of a single [`cast sig`](https://book.getfoundry.sh/reference/cast/cast-sig) call.

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

- [EIP-8048](https://eips.ethereum.org/EIPS/eip-8048)
- [EIP-165: Standard Interface Detection](https://eips.ethereum.org/EIPS/eip-165)
- [Moccasin documentation](https://cyfrin.github.io/moccasin)
- [Vyper documentation](https://docs.vyperlang.org/)

## License & disclaimer

*This is an unaudited reference implementation for educational and development purposes. It is not production-ready software. Use at your own risk. The authors accept no liability for losses or damages arising from its use or deployment. Contract headers license the code under GNU Affero General Public License v3.0 only.*
