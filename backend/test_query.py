import pandas as pd
from query_engine import execute_query

# Load Excel dataset
df = pd.read_excel(
    "../datasets/Retail-Store-Transactions.xlsx"
)

print("Dataset loaded successfully!")
print("Rows:", len(df))
print("Columns:", len(df.columns))

questions = [
    "What is the total revenue?",
    "What is the average transaction?",
    "Show store revenue",
    "Show sales by location",
    "Show sales by time of day",
    "Show sales by day of the week"
]

for question in questions:

    print("\nQuestion:", question)

    result = execute_query(df, question)

    print("Result:", result)

