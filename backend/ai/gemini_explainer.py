import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# -------------------------------------------------
# ENV + GEMINI CONFIG
# -------------------------------------------------
load_dotenv("backend/.env")

API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("Gemini API key not found in environment variables")

genai.configure(api_key=API_KEY)

MODEL_NAME = "models/gemini-flash-lite-latest"

# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def load_json_safe(path):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def summarize_accessibility(accessibility):
    if not accessibility or "features" not in accessibility:
        return "No accessibility data available."

    total = len(accessibility["features"])
    underserved = sum(
        1
        for f in accessibility["features"]
        if f["properties"].get("underserved") is True
    )

    avg_time = sum(
        f["properties"].get("travel_time_min", 0)
        for f in accessibility["features"]
    ) / max(total, 1)

    return (
        f"Total zones: {total}. "
        f"Underserved zones: {underserved}. "
        f"Average travel time: {avg_time:.1f} minutes."
    )


def summarize_optimization(summary):
    if not summary:
        return "No new hospitals were required."

    return json.dumps(summary, indent=2)


# -------------------------------------------------
# MAIN EXPLANATION FUNCTION
# -------------------------------------------------
def explain_results():
    accessibility = load_json_safe(
        "backend/data/processed/accessibility_results.geojson"
    )

    optimization = load_json_safe(
        "backend/data/processed/optimization_summary.json"
    )

    accessibility_summary = summarize_accessibility(accessibility)
    optimization_summary = summarize_optimization(optimization)

    prompt = f"""
You are an AI assistant explaining healthcare accessibility results
to planners and emergency responders.

IMPORTANT RULES:
- Do NOT recompute routes or optimization.
- Do NOT invent numbers.
- Only explain the provided summaries.

Accessibility Summary:
{accessibility_summary}

Optimization Summary:
{optimization_summary}

Explain clearly:
1. Which areas are underserved and why
2. Emergency response implications
3. Long-term healthcare planning insights

Use simple, non-technical language.
"""

    model = genai.GenerativeModel(model_name=MODEL_NAME)
    response = model.generate_content(prompt)

    return response.text
