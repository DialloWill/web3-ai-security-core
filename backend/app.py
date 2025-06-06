from flask import Flask, request, jsonify
from contract_scanner import scan_contract_logic
from ai_auditor import explain_issues_with_gpt
from dotenv import load_dotenv
from web3 import Web3
import os

app = Flask(__name__)
load_dotenv()  # Load environment variables from .env

# Connect to Ethereum node (e.g., Infura, Alchemy, or local Ganache)
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URL")))

@app.route('/')
def home():
    return "Welcome to the Web3 AI Security Core API! Use /scan or /scan/address."

# ✅ AI-powered smart contract audit with GPT
@app.route('/scan', methods=['POST'])
def scan_contract():
    print("Received request at /scan")
    data = request.get_json()
    print("Request JSON data:", data)
    code = data.get("code")

    if not code:
        return jsonify({"error": "No code provided"}), 400

    # Step 1: Basic static scan
    result = scan_contract_logic(code)

    # Step 2: AI-enhanced GPT audit
    ai_audit = explain_issues_with_gpt(result["issues"], code)

    return jsonify({
        "static_issues": result["issues"],      # From pattern matcher
        "ai_audit": ai_audit                    # From GPT
    })

# ✅ Pull on-chain contract bytecode by address
@app.route('/scan/address', methods=['POST'])
def scan_contract_address():
    print("Received request at /scan/address")
    data = request.get_json()
    print("Request JSON data:", data)
    address = data.get('address')

    if not address or not Web3.isAddress(address):
        return jsonify({"error": "Invalid or missing Ethereum address"}), 400

    try:
        checksum_address = Web3.toChecksumAddress(address)
        bytecode = w3.eth.get_code(checksum_address).hex()

        if bytecode == "0x":
            return jsonify({"error": "No contract found at this address"}), 404

        return jsonify({
            "bytecode": bytecode,
            "issues": ["Smart contract bytecode found. Source code analysis not available via bytecode."]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
