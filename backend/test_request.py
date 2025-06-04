import requests

url = "http://127.0.0.1:5000/scan"
payload = {
    "code": """
    pragma solidity ^0.8.0;

    contract Vulnerable {
        function withdraw() public {
            require(tx.origin == msg.sender);
        }
    }
    """
}

response = requests.post(url, json=payload)
print(response.json())
