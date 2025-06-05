import re

def scan_contract(code):
    issues = []

    # Pattern 1: tx.origin (already implemented)
    if re.search(r'\btx\.origin\b', code):
        issues.append("Use of tx.origin for authentication is insecure.")

    # Pattern 2: Reentrancy
    if re.search(r'\.call\{?value:', code) or re.search(r'\.call\.value\(', code):
        issues.append("Potential reentrancy vulnerability detected (use of call.value or .call{value}).")

    # Pattern 3: Unchecked math (only flag if Solidity <0.8.0)
    if re.search(r'pragma solidity\s+<\s*0\.8', code):
        if re.search(r'\b(\w+)\s*[\+\-\*]\s*(\w+)\b', code):
            issues.append("Unchecked arithmetic operations found (consider using SafeMath).")

    return {"issues": issues}
