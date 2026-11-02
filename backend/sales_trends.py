import os
import pandas as pd
import matplotlib.pyplot as plt


def analyze_sales_trends(daily_sales):

    df = daily_sales.copy()

    # Convert Date into datetime format
    df["Date"] = pd.to_datetime(df["Date"])

    # Sort data by date
    df = df.sort_values("Date")

    # Add Year and Month columns
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month

    # Monthly Sales Analysis
    monthly_sales = (
        df.groupby(["Year", "Month"])["Daily_Sales"]
        .sum()
        .reset_index()
    )

    monthly_sales["Month_Name"] = pd.to_datetime(
        monthly_sales["Year"].astype(str)
        + "-"
        + monthly_sales["Month"].astype(str)
        + "-01"
    ).dt.strftime("%b %Y")

    # Weekly Sales Analysis
    df["Day_Name"] = df["Date"].dt.day_name()

    weekly_sales = (
        df.groupby("Day_Name")["Daily_Sales"]
        .mean()
        .reindex([
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ])
        .reset_index()
    )

    # Display Monthly Results
    print("\n========== MONTHLY SALES ANALYSIS ==========")

    print(monthly_sales.to_string(index=False))

    best_month = monthly_sales.loc[
        monthly_sales["Daily_Sales"].idxmax()
    ]

    print("\nHighest Sales Month:", best_month["Month_Name"])
    print("Revenue:", round(best_month["Daily_Sales"], 2))

    # Display Weekly Results
    print("\n========== WEEKLY SALES ANALYSIS ==========")

    print(weekly_sales.to_string(index=False))

    best_day = weekly_sales.loc[
        weekly_sales["Daily_Sales"].idxmax()
    ]

    print("\nBest Performing Day:", best_day["Day_Name"])
    print("Average Sales:", round(best_day["Daily_Sales"], 2))

    # Monthly Sales Graph
    plt.figure(figsize=(12, 6))

    plt.plot(
        monthly_sales["Month_Name"],
        monthly_sales["Daily_Sales"],
        marker="o"
    )

    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig("monthly_sales_trend.png")
    plt.show()

    # Weekly Sales Graph
    plt.figure(figsize=(10, 5))

    plt.bar(
        weekly_sales["Day_Name"],
        weekly_sales["Daily_Sales"]
    )

    plt.title("Average Sales by Day of Week")
    plt.xlabel("Day")
    plt.ylabel("Average Daily Sales")
    plt.tight_layout()

    plt.savefig("weekly_sales_trend.png")
    plt.show()


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

    analyze_sales_trends(daily_sales)