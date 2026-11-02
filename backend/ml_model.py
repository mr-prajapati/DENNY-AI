import os
import pandas as pd

from sklearn.ensemble import RandomForestRegressor , ExtraTreesRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import matplotlib.pyplot as plt

from sklearn.dummy import DummyRegressor
from sklearn.model_selection import GridSearchCV , TimeSeriesSplit    

def train_sales_model(df):

    features = [
        "Year",
        "Month",
        "Day",
        "DayOfWeek",
        "DayOfYear",
        "IsWeekend",
        "Previous_Day_Sales",
        "Previous_7_Days_Sales",
        "Rolling_7_Days_Avg",
        "Rolling_30_Days_Avg"
    ]

    target = "Daily_Sales"

    X = df[features]
    y = df[target]

    # Chronological 80-20 split
    split_index = int(len(df) * 0.8)

    X_train = X.iloc[:split_index]
    X_test = X.iloc[split_index:]

    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    # Define models
    models = {
    "Dummy Regressor": DummyRegressor(strategy="mean"),

    "Random Forest": GridSearchCV(
        estimator=RandomForestRegressor(random_state=42),

        param_grid={
            "n_estimators": [100, 200],
            "max_depth": [None, 10, 20],
            "min_samples_split": [2, 5],
            "min_samples_leaf": [1, 2]
        },

        cv=TimeSeriesSplit(n_splits=3),
        scoring="neg_mean_absolute_error",
        n_jobs=-1
    ),

    "Extra Trees": ExtraTreesRegressor(
        n_estimators=100,
        random_state=42
    )
}

    results = {}
    trained_models = {}
    predictions_dict = {}

    # Train and evaluate each model
    for name, model in models.items():

        model.fit(X_train, y_train)

        if name == "Random Forest":
            print("\nBest Random Forest Parameters:")
            print(model.best_params_)

            trained_models[name] = model.best_estimator_
        else:
            trained_models[name] = model

        predictions = model.predict(X_test)

        mae = mean_absolute_error(y_test, predictions)

        rmse = mean_squared_error(
            y_test, predictions
        ) ** 0.5

        r2 = r2_score(y_test, predictions)

        results[name] = {
            "MAE": round(float(mae), 2),
            "RMSE": round(float(rmse), 2),
            "R2 Score": round(float(r2), 4)
        }

        predictions_dict[name] = predictions

        # Seasonal Naive Forecast (7-day lag)

    seasonal_predictions = y.iloc[
        split_index - 7 : len(y) - 7
    ].values

    seasonal_mae = mean_absolute_error(
        y_test, seasonal_predictions
    )

    seasonal_rmse = mean_squared_error(
        y_test, seasonal_predictions
    ) ** 0.5

    seasonal_r2 = r2_score(
        y_test, seasonal_predictions
    )

    results["Seasonal Naive"] = {
        "MAE": round(float(seasonal_mae), 2),
        "RMSE": round(float(seasonal_rmse), 2),
        "R2 Score": round(float(seasonal_r2), 4)
    }

    predictions_dict["Seasonal Naive"] = seasonal_predictions

    return (
        trained_models,
        results,
        y_test,
        predictions_dict,
        split_index
    )


if __name__ == "__main__":

    from feature_engineering import prepare_features

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

    # Full Calendar Sales Analysis

    calendar_sales = (
        daily_sales
        .set_index("Date")
        .asfreq("D")
        ["Daily_Sales"]
        .fillna(0)
    )

    print("\n========== FULL CALENDAR ANALYSIS ==========")

    print("\nTotal Calendar Days:", len(calendar_sales))

    print(
        "Zero Sales Days:",
        int((calendar_sales == 0).sum())
    )

    print("\nUpdated Sales Statistics:")
    print(calendar_sales.describe().round(2))

    variation = (
        calendar_sales.std() / calendar_sales.mean()
    ) * 100

    print("\nUpdated Sales Variation:", round(variation, 2), "%")
    (
        trained_models,
        results,
        actual,
        predictions_dict,
        split_index
    ) = train_sales_model(featured_df)

    print("\n========== MODEL TRAINING RESULTS ==========")

    print("\nTraining Records:", split_index)
    print("Testing Records:", len(featured_df) - split_index)

    print("\n========== MODEL COMPARISON ==========")

    for model_name, metrics in results.items():

        print(f"\n{model_name}:")

        for metric, value in metrics.items():
            print(f"{metric}: {value}")

    # Select best model based on lowest MAE
    best_model_name = min(
        results,
        key=lambda name: results[name]["MAE"]
    )

    best_model = trained_models[best_model_name]
    best_predictions = predictions_dict[best_model_name]

    print("\n========== BEST MODEL ==========")
    print("Best Model:", best_model_name)
    print("Best MAE:", results[best_model_name]["MAE"])

    # Random Forest Feature Importance
    model = trained_models["Random Forest"]

    feature_importance = pd.Series(
        model.feature_importances_,
        index=model.feature_names_in_
    )

    feature_importance = feature_importance.sort_values(
        ascending=True
    )

    plt.figure(figsize=(10, 6))

    feature_importance.plot(
        kind="barh",
        title="Random Forest Feature Importance"
    )

    plt.xlabel("Importance Score")
    plt.ylabel("Features")

    plt.tight_layout()

    plt.savefig("feature_importance.png")
    plt.show()

    # Best Model: Actual vs Predicted
    plt.figure(figsize=(12, 6))

    plt.plot(
        actual.values,
        label="Actual Sales",
        marker="o"
    )

    plt.plot(
        best_predictions,
        label=f"Predicted Sales ({best_model_name})",
        marker="o"
    )

    plt.title("Actual vs Predicted Daily Sales")
    plt.xlabel("Test Data Records")
    plt.ylabel("Daily Sales")

    plt.legend()
    plt.grid(True)

    plt.tight_layout()

    plt.savefig("sales_prediction_graph.png")
    plt.show()