from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from upload import process_upload
from profiling import profile_data
from generator import generate_synthetic_data, run_attack_test
from privacy import check_privacy
from similarity import check_similarity
from utility import check_utility
from report import generate_report

app = FastAPI()

# Allow your React frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global dictionary to hold datasets in memory (perfect for a quick hackathon build)
db = {
    "original": None,
    "synthetic": None,
    "stats": None,
    "results": None
}

@app.post("/upload")
async def api_upload(file: UploadFile = File(...)):
    contents = await file.read()
    df = process_upload(contents, file.filename)
    
    if df is None:
        return {"error": "Unsupported file format. Please upload CSV, XLSX, or JSON."}
        
    db["original"] = df
    db["stats"] = profile_data(df)
    
    return {"message": "File processed", "stats": db["stats"]}

class GenerateRequest(BaseModel):
    rows: int

@app.post("/generate")
async def api_generate(req: GenerateRequest):
    if db["original"] is None:
        return {"error": "Upload data first"}
        
    # 1. Generate Data
    synth_df = generate_synthetic_data(db["original"], req.rows)
    db["synthetic"] = synth_df
    
    # 2. Run Validations
    priv = check_privacy(db["original"], synth_df)
    sim = check_similarity(db["original"], synth_df)
    util = check_utility(db["original"], synth_df)
    
    # 3. Create Downloadable Report
    generate_report(db["stats"], priv, sim, util)

    # Save results so the frontend can retrieve them
    db["results"] = {
        **priv,
        **sim,
        **util
    }
    return {
        "message": "Generation complete",
        "results": db["results"]
    }
@app.get("/results")
async def get_results():
    if db["results"] is None:
        return {"error": "Generate synthetic data first"}

    return {
        "message": "Results available",
        "results": db["results"]
    }
@app.post("/attack")
async def api_attack():
    """Runs the poison pill memorization check."""
    if db["original"] is None:
        return {"error": "Upload data first"}
    
    result = run_attack_test(db["original"])
    return result

@app.get("/download/data")
async def download_data():
    return FileResponse("outputs/synthetic_data.csv", filename="synthetic_data.csv")

@app.get("/download/report")
async def download_report():
    return FileResponse("outputs/SynthGuard_Report.txt", filename="SynthGuard_Report.txt")