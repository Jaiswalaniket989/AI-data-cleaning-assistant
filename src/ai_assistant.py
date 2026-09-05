import os
import json

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


def generate_ai_recommendations(issues):
    """
    Generate fast AI recommendations using Gemini.

    Gemini receives only the detected data-quality issues,
    not the complete dataset.
    """

    # ========================================================
    # GET API KEY
    # ========================================================

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is not set. "
            "Please check your .env file."
        )


    # ========================================================
    # GEMINI CLIENT
    # ========================================================

    client = OpenAI(
        api_key=api_key,
        base_url=(
            "https://generativelanguage.googleapis.com/"
            "v1beta/openai/"
        )
    )


    # ========================================================
    # PREPARE ONLY IMPORTANT ISSUE DATA
    # ========================================================

    simplified_issues = []

    for issue in issues:

        item = {
            "type": issue.get("type"),
            "column": issue.get("column"),
            "count": issue.get("count"),
            "percentage": issue.get("percentage"),
            "severity": issue.get("severity"),
            "variants": issue.get("variants"),
            "suggested_value": issue.get(
                "suggested_value"
            ),
            "lower_bound": issue.get(
                "lower_bound"
            ),
            "upper_bound": issue.get(
                "upper_bound"
            )
        }

        # Remove empty values
        item = {
            key: value
            for key, value in item.items()
            if value is not None
        }

        simplified_issues.append(item)


    # ========================================================
    # SHORT PROMPT
    # ========================================================

    prompt = f"""
You are a professional Data Quality Engineer.

Analyze ONLY these detected issues:

{json.dumps(simplified_issues, default=str)}

Give a short, practical recommendation for each issue.

Return ONLY valid JSON in this format:

{{
    "summary": "Short overall assessment",
    "recommendations": [
        {{
            "issue_type": "missing_values",
            "column": "age",
            "severity": "medium",
            "recommended_action": "Use median imputation",
            "reason": "Short reason",
            "confidence": 0.95
        }}
    ]
}}

Rules:
- Do not invent issues.
- Do not analyze the complete dataset.
- Keep every reason under 25 words.
- Keep the summary under 40 words.
- Confidence must be between 0 and 1.
"""


    # ========================================================
    # GEMINI REQUEST
    # ========================================================

    try:

        response = client.chat.completions.create(
            model="gemini-3.7-flash",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1
        )


        # ====================================================
        # GET RESPONSE
        # ====================================================

        result = response.choices[0].message.content


        if not result:

            return {
                "summary": "Gemini returned an empty response.",
                "recommendations": []
            }


        result = result.strip()


        # ====================================================
        # REMOVE MARKDOWN CODE BLOCKS
        # ====================================================

        if result.startswith("```json"):

            result = result[7:].strip()

        elif result.startswith("```"):

            result = result[3:].strip()


        if result.endswith("```"):

            result = result[:-3].strip()


        # ====================================================
        # PARSE JSON
        # ====================================================

        return json.loads(result)


    except json.JSONDecodeError:

        return {
            "summary": "Gemini returned invalid JSON.",
            "recommendations": [],
            "raw_response": result
        }


    except Exception as e:

        return {
            "summary": "Gemini analysis failed.",
            "recommendations": [],
            "error": str(e)
        }