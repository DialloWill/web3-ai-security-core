import re

def scan_contract(code):
    vulnerabilities = []

    # Detect reentrancy pattern (simplified)
    if "call.value" in code or "send(" in code:
        vulnerabilities.append("Possible Reentrancy Attack Detected.")

    # Detect use of tx.origin
    if "tx.origin" in code:
        vulnerabilities.append("Use of tx.origin for authentication is insecure.")

    # Detect integer overflows (basic check)
    if "SafeMath" not in code and ("+" in code or "-" in code):
        vulnerabilities.append("No SafeMath library found — Risk of overflow/underflow.")

    return vulnerabilities
