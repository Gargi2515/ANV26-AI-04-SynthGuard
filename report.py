import os

def generate_report(stats, priv, sim, util):
    os.makedirs("outputs", exist_ok=True)
    filepath = "outputs/SynthGuard_Report.txt"
    
    content = f"""
    🛡️ SynthGuard Validation Report 🛡️
    ===================================
    
    1. DATA PROFILING
    -----------------
    Original Rows: {stats.get('rows', 'N/A')}
    Original Columns: {stats.get('columns', 'N/A')}
    
    2. PRIVACY VALIDATION
    ---------------------
    Exact Duplicates Found: {priv.get('exact_duplicates', 'N/A')}
    Privacy Risk Level: {priv.get('risk', 'UNKNOWN')}
    
    3. SIMILARITY & UTILITY
    -----------------------
    Distribution Similarity: {sim.get('distribution_similarity', 0)}%
    Utility Retention: {util.get('utility_retention', 0)}%
    """
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath