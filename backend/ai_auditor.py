import openai
import os
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

def explain_issues_with_gpt(issues, code):
    prompt = f"""
You are a smart contract security auditor. Analyze the following Solidity code.

Tasks:
1. Identify and explain vulnerabilities (e.g., reentrancy, tx.origin, unchecked math).
2. Recommend gas optimizations.
3. Suggest secure code fixes.
4. Output JSON in this exact structure:

{{
  "issues": [
    {{
      "type": "Vulnerability" | "Gas Optimization",
      "title": "Short name of issue",
      "description": "What is the issue and why it matters",
      "line": 42,
      "recommendation": "Advice to fix",
      "fix_code": "Recommended code change (can be pseudocode)"
    }}
  ],
  "trust_score": 0–100
}}

Code:
{code}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a Solidity smart contract security expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        reply = response.choices[0].message['content']
        try:
            return json.loads(reply)
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON", "raw_response": reply}
    except Exception as e:
        return {"error": f"AI error: {str(e)}"}
