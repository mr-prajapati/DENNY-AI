import pandas as pd

def execute_query(df, question):
    question = question.lower().strip()

    # Match column names without case sensitivity
    columns = {
        str(col).strip().lower().replace(" ", "_"): col
        for col in df.columns
    }

    price_col = columns.get("totalprice") or columns.get("total_price")
    store_col = columns.get("storeid")
    location_col = columns.get("location")
    payment_col = columns.get("paymenttype") or columns.get("payment_type")
    time_col = columns.get("timeofday") or columns.get("time_of_day")
    day_col = columns.get("dayofweek") or columns.get("day_of_week")
    transaction_col = columns.get("transactionid") or columns.get("transaction_id")

    if "total rows" in question or "number of rows" in question:
        return {"operation": "Total Rows", "answer": len(df)}

    if "total columns" in question or "number of columns" in question:
        return {"operation": "Total Columns", "answer": len(df.columns)}

    if "total revenue" in question or "total sales" in question:
        if price_col:
            return {
                "operation": "Total Revenue",
                "answer": round(float(df[price_col].sum()), 2)
            }

    if "average transaction" in question:
        if price_col:
            if transaction_col:
                transaction_totals = df.groupby(transaction_col)[price_col].sum()
                average = transaction_totals.mean()
            else:
                average = df[price_col].mean()

            return {
                "operation": "Average Transaction",
                "answer": round(float(average), 2)
            }

    if "payment" in question:
        if payment_col:
            return {
                "operation": "Payment Analysis",
                "answer": df[payment_col].value_counts().to_dict()
            }

    if "store" in question and "revenue" in question:
        if store_col and price_col:
            return {
                "operation": "Store Revenue",
                "answer": df.groupby(store_col)[price_col].sum().round(2).to_dict()
            }

    if "location" in question and ("sales" in question or "revenue" in question):
        if location_col and price_col:
            return {
                "operation": "Location Sales",
                "answer": df.groupby(location_col)[price_col].sum().round(2).to_dict()
            }

    if "time of day" in question:
        if time_col and price_col:
            return {
                "operation": "Time Analysis",
                "answer": df.groupby(time_col)[price_col].sum().round(2).to_dict()
            }

    if "day of the week" in question or "day of week" in question:
        if day_col and price_col:
            return {
                "operation": "Weekly Sales",
                "answer": df.groupby(day_col)[price_col].sum().round(2).to_dict()
            }

    numeric_columns = df.select_dtypes(include="number").columns.tolist()

    if ("maximum" in question or "highest" in question) and numeric_columns:
        return {
            "operation": "Maximum Values",
            "answer": df[numeric_columns].max().to_dict()
        }

    if ("minimum" in question or "lowest" in question) and numeric_columns:
        return {
            "operation": "Minimum Values",
            "answer": df[numeric_columns].min().to_dict()
        }

    if "missing values" in question:
        return {
            "operation": "Missing Values",
            "answer": df.isnull().sum().to_dict()
        }

    if "duplicate" in question:
        return {
            "operation": "Duplicate Rows",
            "answer": int(df.duplicated().sum())
        }

    return {
        "operation": "Not Supported",
        "answer": "This question is not supported yet."
    }