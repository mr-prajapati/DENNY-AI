import os
import pandas as pd


def prepare_features(daily_sales):

    # Create a copy of original data
    df = daily_sales.copy()

    # Convert Date into datetime format
    df["Date"] = pd.to_datetime(df["Date"])

    # Sort data by date
    df = df.sort_values("Date")

    # Add missing calendar dates and set their sales to zero
    df = (
        df.set_index("Date")
        .asfreq("D")
        .fillna({"Daily_Sales": 0})
        .reset_index()
    )

    # Calendar Features
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Day"] = df["Date"].dt.day
    df["DayOfWeek"] = df["Date"].dt.dayofweek
    df["DayOfYear"] = df["Date"].dt.dayofyear

    df["IsWeekend"] = (
        df["DayOfWeek"] >= 5
    ).astype(int)

    # Lag Features
    df["Previous_Day_Sales"] = (
        df["Daily_Sales"].shift(1)
    )

    df["Previous_7_Days_Sales"] = (
        df["Daily_Sales"].shift(7)
    )

    # Rolling Average Features
    df["Rolling_7_Days_Avg"] = (
        df["Daily_Sales"]
        .shift(1)
        .rolling(window=7)
        .mean()
    )

    df["Rolling_30_Days_Avg"] = (
        df["Daily_Sales"]
        .shift(1)
        .rolling(window=30)
        .mean()
    )

    # Remove rows having missing feature values
    df = df.dropna().reset_index(drop=True)

    return df


if __name__ == "__main__":

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    FILE_PATH = os.path.abspath(
        os.path.join(
            BASE_DIR,
            "..",
            "datasets",
            "Retail-Store-Transactions.xlsx"
        )
    )

    raw_df = pd.read_excel(FILE_PATH)

    raw_df["Date"] = pd.to_datetime(
        raw_df["Date"], errors="coerce"
    )

    raw_df["TotalPrice"] = pd.to_numeric(
        raw_df["TotalPrice"], errors="coerce"
    )

    raw_df = raw_df.dropna(
        subset=["Date", "TotalPrice"]
    )

    daily_sales = (
        raw_df.groupby(raw_df["Date"].dt.normalize())["TotalPrice"]
        .sum()
        .reset_index()
    )

    daily_sales.columns = ["Date", "Daily_Sales"]

    featured_df = prepare_features(daily_sales)

    print("\n========== ADVANCED FEATURE ENGINEERING ==========")

    print("\nTotal Records:", len(featured_df))

    print("\nAll Features:")
    print(featured_df.columns.tolist())

    print("\nFirst 5 Records:")
    print(featured_df.head())

    print("\nMissing Values:")
    print(featured_df.isnull().sum())
