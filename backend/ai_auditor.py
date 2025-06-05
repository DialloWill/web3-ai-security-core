import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def explain_issues_with_gpt(issues, code):
    if not issues:
        return {"explanations": "✅ No known issues found."}

    prompt = f"""
You are a smart contract security auditor. Explain the following vulnerabilities found in this Solidity code, and suggest secure fixes for each:

Code:
{code}

Vulnerabilities:
{', '.join(issues)}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a Solidity smart contract security expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return {"explanations": response.choices[0].message['content']}
    except Exception as e:
        return {"explanations": f"AI error: {str(e)}"}
