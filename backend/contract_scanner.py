import re

def scan_contract_logic(code):
    issues = []

    if "tx.origin" in code:
        issues.append("Use of tx.origin for authentication is insecure.")
    if "call.value" in code or "call{" in code:
        issues.append("Potential reentrancy vulnerability.")
    if "unchecked" in code or "SafeMath" not in code:
        issues.append("Unchecked math operations can cause overflows.")

    return {"issues": issues}
