from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from explanation_module import explain_concept
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


# --------------------------------------------------
# PROJECT PATH
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent


# --------------------------------------------------
# FASTAPI APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="EduGenie",
    version="1.0.0",
    description="Google Gemini powered educational learning assistant.",
)


# --------------------------------------------------
# STATIC FILES
# --------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)


# --------------------------------------------------
# HTML TEMPLATES
# --------------------------------------------------

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# --------------------------------------------------
# REQUEST MODELS
# --------------------------------------------------

class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=20000,
    )


class QuizRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=20000,
    )

    count: int = Field(
        default=3,
        ge=1,
        le=10,
    )


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request},
    )


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "EduGenie",
    }


# --------------------------------------------------
# QUESTION ANSWERING
# --------------------------------------------------

@app.post("/qa")
async def qa(payload: TextRequest):
    try:
        result = answer_question(payload.text)

        return {
            "result": result
        }

    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={
                "detail": str(exc)
            },
        )


# --------------------------------------------------
# CONCEPT EXPLANATION
# --------------------------------------------------

@app.post("/explain")
async def explain(payload: TextRequest):
    try:
        result = explain_concept(payload.text)

        return {
            "result": result
        }

    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={
                "detail": str(exc)
            },
        )


# --------------------------------------------------
# QUIZ GENERATION
# --------------------------------------------------

@app.post("/quiz")
async def quiz(payload: QuizRequest):
    try:
        result = generate_quiz(
            payload.text,
            payload.count,
        )

        return {
            "result": result
        }

    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={
                "detail": str(exc)
            },
        )


# --------------------------------------------------
# SUMMARIZATION
# --------------------------------------------------

@app.post("/summarize")
async def summarize(payload: TextRequest):
    try:
        result = summarize_text(payload.text)

        return {
            "result": result
        }

    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={
                "detail": str(exc)
            },
        )


# --------------------------------------------------
# LEARNING PATH
# --------------------------------------------------

@app.post("/learn/recommendations")
async def learning_recommendations(payload: TextRequest):
    try:
        result = get_learning_recommendations(payload.text)

        return {
            "result": result
        }

    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={
                "detail": str(exc)
            },
        )