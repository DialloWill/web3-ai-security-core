from flask import request
from web3 import Web3

# Connect to Infura (or another Ethereum provider)
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'))  # Replace this

@app.route('/scan/address', methods=['POST'])
def scan_contract_address():
    data = request.get_json()
    address = data.get('address')
    if not address or not w3.isAddress(address):
        return jsonify({"error": "Invalid or missing Ethereum address"}), 400

    try:
        contract = w3.eth.get_code(Web3.toChecksumAddress(address)).hex()
        if contract == "0x":
            return jsonify({"error": "No contract found at this address"}), 404

        return jsonify({"issues": ["Smart contract bytecode found. Source code analysis not available via bytecode."]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
