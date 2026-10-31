import pandas as pd


def analyze_dataset(df):

    # Basic Information
    total_rows = len(df)
    total_columns = len(df.columns)

    # Data Types
    data_types = {
        col: str(dtype)
        for col, dtype in df.dtypes.items()
    }

    # Missing Values
    missing_values = {
        col: int(value)
        for col, value in df.isnull().sum().items()
    }

    # Duplicate Records
    duplicate_rows = int(df.duplicated().sum())

    # Numerical Columns
    numerical_df = df.select_dtypes(include="number")

    numerical_summary = {}

    if not numerical_df.empty:
        numerical_summary = (
            numerical_df.describe()
            .round(2)
            .to_dict()
        )

    # Categorical Columns
    categorical_df = df.select_dtypes(
        include=["object", "category"]
    )

    categorical_summary = {}

    for col in categorical_df.columns:
        categorical_summary[col] = {
            "unique_values": int(df[col].nunique()),
            "most_frequent": (
                str(df[col].mode().iloc[0])
                if not df[col].mode().empty
                else None
            )
        }

    return {
        "total_rows": total_rows,
        "total_columns": total_columns,
        "data_types": data_types,
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "numerical_summary": numerical_summary,
        "categorical_summary": categorical_summary
    }