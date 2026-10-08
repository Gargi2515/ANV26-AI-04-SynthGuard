import pandas as pd
import os

def process_upload(file_bytes: bytes, filename: str):
    os.makedirs("uploads", exist_ok=True)
    filepath = os.path.join("uploads", filename)
    
    with open(filepath, "wb") as f:
        f.write(file_bytes)
        
    if filename.endswith('.csv'):
        return pd.read_csv(filepath)
    elif filename.endswith('.xlsx'):
        return pd.read_excel(filepath)
    elif filename.endswith('.json'):
        return pd.read_json(filepath)
    return None