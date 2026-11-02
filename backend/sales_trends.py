import os
import pandas as pd
import matplotlib.pyplot as plt


def analyze_sales_trends(daily_sales):

    df = daily_sales.copy()

    # Convert Date into datetime format
    df["Date"] = pd.to_datetime(df["Date"])

    # Sort data by date
    df = df.sort_values("Date")
    # Include all calendar dates
    df = (
        df.set_index("Date")
        .asfreq("D")
        .fillna({"Daily_Sales": 0})
        .reset_index()
    )

    # Add Year and Month columns
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month

    # Zero Sales Days Analysis
    zero_sales_days = df[df["Daily_Sales"] == 0]

    non_zero_sales_days = df[df["Daily_Sales"] > 0]

    print("\n========== ZERO SALES ANALYSIS ==========")

    print("Total Calendar Days:", len(df))
    print("Zero Sales Days:", len(zero_sales_days))
    print("Non-Zero Sales Days:", len(non_zero_sales_days))

    zero_percentage = (
        len(zero_sales_days) / len(df)
    ) * 100

    print("Zero Sales Percentage:", round(zero_percentage, 2), "%")

    print("\nZero Sales Dates:")

    print(
        zero_sales_days["Date"].dt.strftime("%Y-%m-%d").to_list()
    )

    # Zero Sales Pattern Analysis

    zero_sales_days["Day_Name"] = (
        zero_sales_days["Date"].dt.day_name()
    )

    zero_sales_days["Month_Name"] = (
        zero_sales_days["Date"].dt.strftime("%b %Y")
    )

    print("\n========== ZERO SALES BY WEEKDAY ==========")

    print(
        zero_sales_days["Day_Name"]
        .value_counts()
    )

    print("\n========== ZERO SALES BY MONTH ==========")

    print(
        zero_sales_days["Month_Name"]
        .value_counts()
    )

    # Consecutive Zero Sales Analysis

    zero_dates = zero_sales_days["Date"].sort_values()

    zero_date_groups = (
        zero_dates.diff().dt.days.ne(1).cumsum()
    )

    consecutive_groups = zero_dates.groupby(
        zero_date_groups
    )

    print("\n========== CONSECUTIVE ZERO SALES DAYS ==========")

    for _, dates in consecutive_groups:

        if len(dates) >= 2:

            print(
                "From:",
                dates.iloc[0].date(),
                "To:",
                dates.iloc[-1].date(),
                "| Consecutive Days:",
                len(dates)
            )

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

    # Advanced Sales Insights

    monthly_sales = monthly_sales.sort_values(
        ["Year", "Month"]
    ).copy()

    # Month-over-Month Growth
    monthly_sales["MoM_Growth_Percent"] = (
        monthly_sales["Daily_Sales"]
        .pct_change(fill_method=None) * 100
    )

    # Year-over-Year Growth
    previous_year_sales = monthly_sales[
        ["Year", "Month", "Daily_Sales"]
    ].copy()

    previous_year_sales["Year"] += 1

    previous_year_sales = previous_year_sales.rename(
        columns={
            "Daily_Sales": "Previous_Year_Sales"
        }
    )

    monthly_sales = monthly_sales.merge(
        previous_year_sales,
        on=["Year", "Month"],
        how="left"
    )

    monthly_sales["YoY_Growth_Percent"] = (
        (
            monthly_sales["Daily_Sales"]
            - monthly_sales["Previous_Year_Sales"]
        )
        / monthly_sales["Previous_Year_Sales"]
    ) * 100

    print("\n========== MONTH-OVER-MONTH GROWTH ==========")

    print(
        monthly_sales[
            ["Month_Name", "Daily_Sales", "MoM_Growth_Percent"]
        ].round(2).to_string(index=False)
    )

    print("\n========== YEAR-OVER-YEAR GROWTH ==========")

    print(
        monthly_sales[
            ["Month_Name", "Daily_Sales", "YoY_Growth_Percent"]
        ].round(2).to_string(index=False)
    )

    # Highest and Lowest Revenue Month
    highest_month = monthly_sales.loc[
        monthly_sales["Daily_Sales"].idxmax()
    ]

    lowest_month = monthly_sales.loc[
        monthly_sales["Daily_Sales"].idxmin()
    ]

    print("\n========== REVENUE PERFORMANCE ==========")

    print(
        "Highest Revenue Month:",
        highest_month["Month_Name"],
        "| Revenue:",
        round(highest_month["Daily_Sales"], 2)
    )

    print(
        "Lowest Revenue Month:",
        lowest_month["Month_Name"],
        "| Revenue:",
        round(lowest_month["Daily_Sales"], 2)
    )

    # Monthly Sales Volatility
    monthly_mean = monthly_sales["Daily_Sales"].mean()

    monthly_std = monthly_sales["Daily_Sales"].std()

    monthly_volatility = (
        monthly_std / monthly_mean
    ) * 100

    print("\n========== SALES VOLATILITY ==========")

    print(
        "Monthly Sales Volatility:",
        round(monthly_volatility, 2),
        "%"
    )

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