import pandas as pd
import os
import time

def generate_synthetic_data(df, target_rows):
    # TODO: Replace with NVIDIA NeMo Data Designer API
    time.sleep(1.5) # Simulating API latency for the UI
    
    # Mock generation: sample and add 1% noise to numerical columns to prevent exact copies
    synth_df = df.sample(n=target_rows, replace=True).reset_index(drop=True)
    num_cols = synth_df.select_dtypes(include='number').columns
    for col in num_cols:
        synth_df[col] = synth_df[col] * 1.01 
    
    os.makedirs("outputs", exist_ok=True)
    synth_df.to_csv("outputs/synthetic_data.csv", index=False)
    
    return synth_df

def run_attack_test(df):
    """Injects a recognizable 'poison pill' to test for data memorization."""
    poison_row = df.iloc[0].copy()
    num_cols = df.select_dtypes(include='number').columns
    
    # Inject a crazy, unmistakable value into all numerical columns
    for col in num_cols:
        poison_row[col] = 9999999.99
    
    # Add the poison pill to the original data
    attack_df = pd.concat([df, pd.DataFrame([poison_row])], ignore_index=True)
    
    # Run the generator on the poisoned data
    attack_synth = generate_synthetic_data(attack_df, len(attack_df))
    
    # Check if the extreme value was memorized and spit out by the generator
    if len(num_cols) > 0:
        memorized = attack_synth[attack_synth[num_cols[0]] == 9999999.99].shape[0] > 0
    else:
        memorized = False
        
    return {"attack_defeated": not memorized}