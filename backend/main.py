from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from io import BytesIO
from eda import analyze_dataset
from data_cleaning import clean_dataset 
from visualization import generate_visualizations
from pydantic import BaseModel
from ai_analysis import ask_ai_about_data

# Create FastAPI application
app = FastAPI(
    title="DENNY AI",
    description="Intelligent Data Analysis Platform",
    version="1.0.0"
)

# Home route
@app.get("/")
def home():
    return {
        "message": "Welcome to DataMind AI!",
        "status": "Backend is running successfully"
    }

# Health check route
@app.get("/health")
def health_check():
    return {
        "status": "Healthy"
    }

@app.post("/upload-dataset")
async def upload_dataset(file: UploadFile = File(...)):

    filename = file.filename.lower()

    try:
        contents = await file.read()

        if filename.endswith(".csv"):
            df = pd.read_csv(BytesIO(contents))

        elif filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(BytesIO(contents))

        else:
            raise HTTPException(
                status_code=400,
                detail="Only CSV and Excel files are supported."
            )

        return {
            "filename": file.filename,
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "columns": list(df.columns),
            "missing_values": {
                col: int(count)
                for col, count in df.isnull().sum().items()
            },
            "duplicate_rows": int(df.duplicated().sum()),
            "preview": df.head(5).astype(object).where(
                pd.notna(df.head(5)), None
            ).to_dict(orient="records")
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error processing file: {str(e)}"
        )

@app.post("/analyze-dataset")
async def analyze_file(file: UploadFile = File(...)):

    contents = await file.read()
    filename = file.filename.lower()

    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(BytesIO(contents))

        elif filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(BytesIO(contents))

        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file format"
            )

        if df.empty:
            raise HTTPException(
                status_code=400,
                detail="Dataset is empty"
            )

        result = analyze_dataset(df)

        return result

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@app.post("/clean-dataset")
async def clean_file(file: UploadFile = File(...)):

    contents = await file.read()
    filename = file.filename.lower()

    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(BytesIO(contents))

        elif filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(BytesIO(contents))

        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file format"
            )

        if df.empty:
            raise HTTPException(
                status_code=400,
                detail="Dataset is empty"
            )

        cleaned_df, report = clean_dataset(df)

        return {
            "message": "Dataset cleaned successfully",
            "cleaning_report": report,
            "cleaned_preview": cleaned_df.head(5).astype(
                object
            ).where(
                pd.notna(cleaned_df.head(5)), None
            ).to_dict(orient="records")
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@app.post("/visualize-dataset")
async def visualize_file(file: UploadFile = File(...)):

    contents = await file.read()
    filename = file.filename.lower()

    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(BytesIO(contents))

        elif filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(BytesIO(contents))

        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file format"
            )

        if df.empty:
            raise HTTPException(
                status_code=400,
                detail="Dataset is empty"
            )

        charts = generate_visualizations(df)

        return {
            "message": "Visualizations generated successfully",
            "charts": charts
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

class AIQuestion(BaseModel):
    question: str


@app.post("/ask-ai")
async def ask_question(
    file: UploadFile = File(...),
    question: str = ""
):

    contents = await file.read()
    filename = file.filename.lower()

    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(BytesIO(contents))

        elif filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(BytesIO(contents))

        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file format"
            )

        if df.empty:
            raise HTTPException(
                status_code=400,
                detail="Dataset is empty"
            )

        answer = ask_ai_about_data(df, question)

        return {
            "question": question,
            "answer": answer
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )