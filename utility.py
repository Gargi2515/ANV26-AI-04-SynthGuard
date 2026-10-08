from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

def check_utility(original_df, synth_df):
    orig_clean = original_df.select_dtypes(include='number').dropna()
    synth_clean = synth_df.select_dtypes(include='number').dropna()
    
    if orig_clean.shape[1] < 2:
        return {"utility_retention": 0}
        
    # Pick the last numerical column to act as our dummy target for ML training
    target_col = orig_clean.columns[-1] 
    X_orig = orig_clean.drop(columns=[target_col])
    
    # Convert target to binary classification (above/below median)
    y_orig = orig_clean[target_col] > orig_clean[target_col].median()
    
    X_train, X_test, y_train, y_test = train_test_split(X_orig, y_orig, test_size=0.2, random_state=42)
    
    try:
        # Train on real data
        model_real = RandomForestClassifier(n_estimators=10, random_state=42).fit(X_train, y_train)
        acc_real = accuracy_score(y_test, model_real.predict(X_test))
        
        # Train on synthetic data
        X_synth = synth_clean[X_orig.columns]
        y_synth = synth_clean[target_col] > synth_clean[target_col].median()
        model_synth = RandomForestClassifier(n_estimators=10, random_state=42).fit(X_synth, y_synth)
        
        # Test synthetic model on REAL test data
        acc_synth = accuracy_score(y_test, model_synth.predict(X_test))
        
        # Calculate how much accuracy we kept
        retention = min(acc_synth / acc_real * 100, 100) if acc_real > 0 else 0
        return {"utility_retention": round(retention, 1)}
    except Exception:
        return {"utility_retention": 0}