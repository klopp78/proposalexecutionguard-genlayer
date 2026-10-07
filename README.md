# ProposalExecutionGuard for GenLayer

ProposalExecutionGuard is a reusable GenLayer Intelligent Contract that creates evidence-bound receipts showing whether a governance proposal was executed exactly as approved. It is designed for DAO treasuries, timelocks, governance dashboards, autonomous agents, and cross-chain execution monitors.

## Why it matters

A proposal passing and a transaction succeeding are separate facts. The execution may omit an approved call, add an unapproved transfer, change a target or parameter, fail on-chain, or belong to another proposal. This contract binds the proposal identity, approved action text, execution transaction, independently rendered evidence, and accepted assessment into one persistent receipt.

## Consensus design

Callers provide the governance name, proposal ID, canonical proposal URL, canonical execution transaction URL, declared approved actions, and two to five public evidence sources on at least two independent domains. The proposal and transaction URLs must be included in the source bundle.

Every validator independently renders every source and compares all consequential fields:

- proposal and execution status;
- exact proposal, action, and transaction matches;
- target chain and execution timestamp;
- supporting and readable source counts;
- every SHA-256 source snapshot hash;
- snapshot bundle and assessment context commitments.

An `executed_match` receipt requires a passed proposal, successful transaction, exact proposal/action/transaction matches, a timestamp, and at least two supporting sources. Confirmed execution transaction URLs are claimable only once, preventing receipt replay.

## Persistent API

```python
assess_execution(governance_name, proposal_id, proposal_url, execution_tx_url, declared_actions, source_urls) -> str
get_assessment(assessment_id) -> str
get_latest_assessment_id() -> str
get_assessment_count() -> u64
list_assessment_ids() -> str
get_execution_claim(execution_tx_url) -> str
```

Accepted writes receive a `peg_*` ID and are preserved in an append-only registry with cryptographic record, source snapshot, action, execution-reference, and context commitments.

## Verification

```bash
python scripts/check_contract.py
python -m unittest discover -s tests -v
```

## Studio deployment

- Contract: `0xA972D14f7029a6263645DB72ca46eeF81e088280`
- Explorer: https://explorer-studio.genlayer.com/address/0xA972D14f7029a6263645DB72ca46eeF81e088280
- Verified receipt: `peg_443f8cba63e00ce90477`

The first finalized assessment checks Aave Governance proposal 359 against its Ethereum execution transaction. Validators received the official Aave proposal page, the Etherscan transaction, and the Aave governance discussion as independent public evidence:

- https://vote.onaave.com/proposal/?ipfsHash=0x5c6bcd27cc94e27f40112647e0fde323c17706ce82746008ceae9d707deb0208&proposalId=359
- https://etherscan.io/tx/0x7a41b0b367d7914389edfdf132c9031fb6379bb97e7b6b0139c02ffd087f1ded
- https://governance.aave.com/t/arfc-claiming-aave-rewards-for-the-sablier-legacy-v1-1-contract/21975

The deployed source matches `contracts/proposal_execution_guard.py`.
