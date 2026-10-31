import pandas as pd


def clean_dataset(df):

    original_rows = len(df)

    # Count missing values before cleaning
    missing_before = int(df.isnull().sum().sum())

    # Count duplicate rows
    duplicates_before = int(df.duplicated().sum())

    # Remove duplicate rows
    df = df.drop_duplicates().copy()

    # Separate numerical and categorical columns
    numerical_columns = df.select_dtypes(
        include="number"
    ).columns

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns

    # Fill numerical missing values with median
    for col in numerical_columns:
        median_value = df[col].median()

        if pd.notna(median_value):
            df[col] = df[col].fillna(median_value)

    # Fill categorical missing values with mode
    for col in categorical_columns:
        mode_value = df[col].mode()

        if not mode_value.empty:
            df[col] = df[col].fillna(mode_value.iloc[0])

    # Final missing values
    missing_after = int(df.isnull().sum().sum())

    report = {
        "original_rows": original_rows,
        "final_rows": len(df),
        "duplicates_removed": duplicates_before,
        "missing_values_before": missing_before,
        "missing_values_after": missing_after,
        "rows_removed": original_rows - len(df)
    }

    return df, report