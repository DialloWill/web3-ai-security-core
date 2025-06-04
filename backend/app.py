from flask import Flask, request, jsonify
from contract_scanner import scan_contract

app = Flask(__name__)

@app.route("/scan", methods=["POST"])
def scan():
    data = request.get_json()
    code = data.get("code", "")

    if not code:
        return jsonify({"error": "No smart contract code provided."}), 400

    results = scan_contract(code)
    return jsonify({"issues": results})

if __name__ == "__main__":
    app.run(debug=True)
