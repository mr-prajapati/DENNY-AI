import pandas as pd


def execute_query(df, question):

    question = question.lower().strip()

    result = {}

    # 1. Total rows
    if "total rows" in question or "number of rows" in question:
        result = {
            "operation": "Total Rows",
            "answer": len(df)
        }

    # 2. Total columns
    elif "total columns" in question or "number of columns" in question:
        result = {
            "operation": "Total Columns",
            "answer": len(df.columns)
        }

    # 3. Missing values
    elif "missing values" in question or "null values" in question:
        result = {
            "operation": "Missing Values",
            "answer": df.isnull().sum().to_dict()
        }

    # 4. Duplicate rows
    elif "duplicate rows" in question:
        result = {
            "operation": "Duplicate Rows",
            "answer": int(df.duplicated().sum())
        }

    # 5. Numerical statistics
    elif "average" in question or "mean" in question:
        numerical_df = df.select_dtypes(include="number")

        result = {
            "operation": "Average",
            "answer": numerical_df.mean().round(2).to_dict()
        }

    elif "maximum" in question or "highest" in question:
        numerical_df = df.select_dtypes(include="number")

        result = {
            "operation": "Maximum",
            "answer": numerical_df.max().to_dict()
        }

    elif "minimum" in question or "lowest" in question:
        numerical_df = df.select_dtypes(include="number")

        result = {
            "operation": "Minimum",
            "answer": numerical_df.min().to_dict()
        }

    # 6. Dataset columns
    elif "column names" in question or "columns" in question:
        result = {
            "operation": "Column Names",
            "answer": df.columns.tolist()
        }

    else:
        result = {
            "operation": "Not Supported",
            "answer": "This question is not supported by the current query engine."
        }

    return result