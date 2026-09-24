# Bug Bounty PoC - DeFi Vault Fee Validation Bypass

## Researcher
**AXS-X-SECURITY** | Ethical Hacker from Gedaref, Sudan | Focus: DeFi / Smart Contract Security

## Vulnerability Description
**Type:** Missing Fee Cap Validation / Admin Rug Risk
**Severity:** High / Critical
**Location:** `setFee()` function - No upper bound check

The admin can set fee > 100% (e.g., 10000 basis points), allowing 100% of user deposits to be drained as "fees".

## Impact
- Complete loss of user funds if admin key compromised or malicious
- Violates trust assumption of capped fees

## PoC
```solidity
// PoC - Fee can be set to 100%
vault.setFee(10000); // 100% - No revert
// User deposits 1000 USDC -> 1000 goes to admin