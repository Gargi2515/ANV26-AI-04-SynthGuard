def profile_data(df):
    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "missing": int(df.isna().sum().sum()),
        "duplicates": int(df.duplicated().sum()),
        "num_cols": int(len(df.select_dtypes(include='number').columns)),
        "cat_cols": int(len(df.select_dtypes(include=['object', 'category']).columns))
    }
