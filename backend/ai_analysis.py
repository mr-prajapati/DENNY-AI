import os
import json
from google import genai


def ask_ai_about_data(df, question):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "Gemini API key is missing."

    client = genai.Client(api_key=api_key)

    # Generate dataset summary
    summary = {
        "columns": list(df.columns),
        "total_rows": len(df),
        "data_types": df.dtypes.astype(str).to_dict(),
        "statistics": json.loads(
            df.describe(include="all").to_json()
        ),
        "sample_data": json.loads(
            df.head(10).to_json(orient="records")
        )
    }

    prompt = f"""
    You are DataMind AI, an intelligent data analyst.

    Analyze the following dataset information.

    Dataset:
    {json.dumps(summary, default=str)}

    User Question:
    {question}

    Instructions:
    1. Answer based on the provided dataset.
    2. Do not invent statistics.
    3. If information is insufficient, clearly say so.
    4. Explain insights in simple English.
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text