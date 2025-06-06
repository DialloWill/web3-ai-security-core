import openai
import os
import json

# Load your OpenAI API key from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

def explain_issues_with_gpt(issues, code):
    """
    Use GPT to audit the provided Solidity code and return structured vulnerability and optimization data.
    """
    if not issues:
        return {
            "issues": [],
            "trust_score": 95  # High trust if no issues statically detected
        }

    # Prompt for GPT auditing
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
            model="gpt-4o",  # You can change to "gpt-4" or another model
            messages=[
                {"role": "system", "content": "You are a Solidity smart contract security expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        # Extract GPT response
        reply = response.choices[0].message['content']

        try:
            parsed = json.loads(reply)
            return parsed
        except json.JSONDecodeError:
            return {
                "error": "Failed to parse JSON from GPT.",
                "raw_response": reply
            }

    except Exception as e:
        return {
            "error": f"AI error: {str(e)}"
        }

