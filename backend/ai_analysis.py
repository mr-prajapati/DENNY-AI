import os
import json
import pandas as pd
from google import genai


def ask_ai_about_data(df, question):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "Gemini API key is missing."

    client = genai.Client(api_key=api_key)

    # 1. Basic dataset information
    summary = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "columns": list(df.columns),
        "data_types": df.dtypes.astype(str).to_dict()
    }

    # 2. Missing values
    summary["missing_values"] = (
        df.isnull().sum().to_dict()
    )

    # 3. Numerical analysis
    numerical_df = df.select_dtypes(include="number")

    if not numerical_df.empty:

        summary["numerical_statistics"] = (
            numerical_df.describe().round(2).to_dict()
        )

    # 4. Categorical analysis
    categorical_df = df.select_dtypes(
        include=["object", "category"]
    )

    categorical_summary = {}

    for col in categorical_df.columns:

        categorical_summary[col] = {
            "unique_values": int(df[col].nunique()),
            "top_10_values": (
                df[col].value_counts()
                .head(10)
                .to_dict()
            )
        }

    summary["categorical_analysis"] = categorical_summary

    # 5. Correlation analysis
    if len(numerical_df.columns) >= 2:

        summary["correlation"] = (
            numerical_df.corr().round(2).to_dict()
        )

    # 6. Sample data
    summary["sample_data"] = (
        df.head(5).to_dict(orient="records")
    )

    # 7. AI Prompt
    prompt = f"""
    You are DataMind AI, an intelligent data analyst.

    Analyze the following dataset information.

    DATASET INFORMATION:
    {json.dumps(summary, default=str)}

    USER QUESTION:
    {question}

    INSTRUCTIONS:

    1. Answer using the provided dataset information.
    2. Numerical statistics are calculated from the complete dataset.
    3. Never invent numbers or statistics.
    4. Clearly mention when information is insufficient.
    5. Explain insights in simple English.
    6. Give practical business insights wherever possible.
    7. Use headings and bullet points for readability.

    Provide an accurate and useful answer.
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text