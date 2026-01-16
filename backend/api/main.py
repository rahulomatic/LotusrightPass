from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import subprocess
import os
import json
from backend.ai.gemini_explainer import explain_results

app = FastAPI(
    title="Smart Healthcare Accessibility Optimizer",
    description="API for accessibility analysis, hospital optimization, and visualization",
    version="1.0"
)

# -----------------------------
# PATH CONFIG
# -----------------------------
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

MAP_FILE = os.path.join(
    PROCESSED_DIR, "healthcare_accessibility_map.html"
)

SUMMARY_FILE = os.path.join(
    PROCESSED_DIR, "optimization_summary.json"
)

# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.get("/health")
def health():
    return {"status": "running"}

# -----------------------------
# RUN ACCESSIBILITY (Milestone 2)
# -----------------------------
@app.post("/run/accessibility")
def run_accessibility():
    try:
        subprocess.run(
            ["python", "backend/analysis/run_accessibility_optimized.py"],
            check=True
        )
        return {"message": "Accessibility analysis completed"}
    except subprocess.CalledProcessError:
        raise HTTPException(
            status_code=500,
            detail="Accessibility analysis failed"
        )

# -----------------------------
# RUN OPTIMIZATION (Milestone 3)
# -----------------------------
@app.post("/run/optimization")
def run_optimization():
    try:
        subprocess.run(
            ["python", "backend/optimization/run_optimization.py"],
            check=True
        )
        return {"message": "Optimization completed"}
    except subprocess.CalledProcessError:
        raise HTTPException(
            status_code=500,
            detail="Optimization failed"
        )

# -----------------------------
# GET MAP (Milestone 4)
# -----------------------------
@app.get("/map")
def get_map():
    if not os.path.exists(MAP_FILE):
        raise HTTPException(
            status_code=404,
            detail="Map not found. Run analysis first."
        )

    return FileResponse(
        MAP_FILE,
        media_type="text/html"
    )

# -----------------------------
# GET SUMMARY
# -----------------------------
@app.get("/summary")
def get_summary():
    if not os.path.exists(SUMMARY_FILE):
        return JSONResponse(
            {"message": "No optimization summary available"},
            status_code=200
        )

    with open(SUMMARY_FILE) as f:
        data = json.load(f)

    return data

# -----------------------------
# AI EXPLANATION (Gemini)
# -----------------------------
@app.get("/ai/explain")
def ai_explain():
    try:
        explanation = explain_results()
        return {"explanation": explanation}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Gemini explanation failed: {str(e)}"
        )