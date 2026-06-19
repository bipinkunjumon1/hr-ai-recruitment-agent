import json
import re
from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

PROMPT = """You are an Interview Email Classification Agent.
Classify the email into exactly one type:
1. reschedule  - candidate wants to change interview date/time
2. confirmation - candidate confirms/accepts the interview
3. rejection   - candidate declines the interview
4. other       - anything else

Return ONLY valid JSON, no extra text:
{{"email_type": "reschedule", "confidence": 95, "reason": "Medical emergency"}}

Email subject: {subject}
Email body: {body}
"""


def classify_email(subject: str, body: str) -> dict:
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user",
                   "content": PROMPT.format(subject=subject, body=body)}],
        temperature=0,
    )
    text = completion.choices[0].message.content
    # Strip markdown fences if the model wraps JSON
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    return {"email_type": "other", "confidence": 0, "reason": "Parse failed"}
