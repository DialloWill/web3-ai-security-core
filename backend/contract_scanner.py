import re

# 🚨 Example: A very simple smart contract vulnerability scanner
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


# 🔬 Test code (you can remove or replace this)
if __name__ == "__main__":
    sample_code = """
    pragma solidity ^0.8.0;

    contract Vulnerable {
        address public owner;

        constructor() {
            owner = msg.sender;
        }

        function withdraw() public {
            require(tx.origin == owner);
            payable(msg.sender).send(address(this).balance);
        }
    }
    """

    issues = scan_contract(sample_code)
    print("Issues found:")
    for issue in issues:
        print("-", issue)
