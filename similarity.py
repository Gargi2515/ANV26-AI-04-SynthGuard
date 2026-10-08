import pandas as pd

def check_similarity(original_df, synth_df):
    num_cols = original_df.select_dtypes(include='number').columns
    if len(num_cols) == 0:
        return {"distribution_similarity": 0}
        
    similarities = []
    for col in num_cols:
        orig_mean = original_df[col].mean()
        orig_std = original_df[col].std()
        
        synth_mean = synth_df[col].mean()
        synth_std = synth_df[col].std()
        
        # Prevent division by zero
        if orig_mean == 0: orig_mean = 0.0001
        if orig_std == 0: orig_std = 0.0001
            
        # Calculate how close the means and standard deviations are
        mean_diff = abs(orig_mean - synth_mean) / abs(orig_mean)
        std_diff = abs(orig_std - synth_std) / abs(orig_std)
        
        # Cap the similarity to a max of 100% and min of 0%
        col_sim = (max(0, 1 - mean_diff) + max(0, 1 - std_diff)) / 2
        similarities.append(col_sim)
        
    avg_sim = sum(similarities) / len(similarities)
    return {"distribution_similarity": round(avg_sim * 100, 1)}