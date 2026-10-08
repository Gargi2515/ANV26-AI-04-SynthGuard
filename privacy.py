import pandas as pd

def check_privacy(original_df, synth_df):
    exact_duplicates = pd.merge(original_df, synth_df, how='inner').shape[0]
    risk = "HIGH" if exact_duplicates > 0 else "LOW"
    return {"exact_duplicates": exact_duplicates, "risk": risk}