from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import re

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Analyze code logic
def analyze_code(content, ext):
    recommendations = []
    score = 100
    breakdown = {"naming": 10, "modularity": 20, "comments": 20, "formatting": 15, "reusability": 15, "best_practices": 20}

    # Naming Convention Check
    if ext == ".py":
        if re.search(r"def [A-Z]", content):
            recommendations.append("Use snake_case for function names in Python.")
            breakdown["naming"] -= 2
    elif ext == ".js" or ext == ".jsx":
        if re.search(r"function [A-Z]", content):
            recommendations.append("Use camelCase for function names in JavaScript.")
            breakdown["naming"] -= 2

    # Check for comments
    if content.count("#" if ext == ".py" else "//") < 2:
        recommendations.append("Add more comments/documentation.")
        breakdown["comments"] -= 5

    # Function length/modularity check
    if len(content.split("\n")) > 30:
        recommendations.append("Refactor long functions to smaller modules.")
        breakdown["modularity"] -= 5

    # Calculate final score
    overall_score = sum(breakdown.values())

    return {
        "overall_score": overall_score,
        "breakdown": breakdown,
        "recommendations": recommendations
    }

# Endpoint to analyze code
@app.post("/analyze-code")
async def analyze_code_endpoint(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1]
    if ext not in [".py", ".js", ".jsx"]:
        return {"error": "Unsupported file type!"}
    
    content = await file.read()
    content_str = content.decode("utf-8")
    result = analyze_code(content_str, ext)
    return result

@app.get("/")
def home():
    return {"message": "Welcome to the AI Code Quality Analyzer! Go to /docs to analyze files."}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
