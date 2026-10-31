import pandas as pd
import plotly.express as px


def generate_visualizations(df):

    charts = {}

    numerical_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    # Bar Chart
    if categorical_columns and numerical_columns:

        fig = px.bar(
            df,
            x=categorical_columns[0],
            y=numerical_columns[0],
            title="Category-wise Analysis"
        )

        charts["bar_chart"] = fig.to_json()

    # Histogram
    if numerical_columns:

        fig = px.histogram(
            df,
            x=numerical_columns[0],
            title="Data Distribution"
        )

        charts["histogram"] = fig.to_json()

    # Scatter Plot
    if len(numerical_columns) >= 2:

        fig = px.scatter(
            df,
            x=numerical_columns[0],
            y=numerical_columns[1],
            title="Relationship Analysis"
        )

        charts["scatter_plot"] = fig.to_json()

    # Pie Chart
    if categorical_columns:

        counts = df[categorical_columns[0]].value_counts().head(10)

        fig = px.pie(
            names=counts.index.astype(str),
            values=counts.values,
            title="Category Distribution"
        )

        charts["pie_chart"] = fig.to_json()

    # Correlation Heatmap
    if len(numerical_columns) >= 2:

        correlation = df[numerical_columns].corr()

        fig = px.imshow(
            correlation,
            text_auto=True,
            title="Correlation Heatmap"
        )

        charts["heatmap"] = fig.to_json()

    return charts