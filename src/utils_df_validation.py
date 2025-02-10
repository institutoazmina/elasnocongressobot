import pandas as pd
from df_config import COLUMNS

def validate_columns(df: pd.DataFrame, dataset: str) -> pd.DataFrame:
    """Ensure DataFrame matches predefined columns."""
    expected_columns = COLUMNS[dataset]
    # Add missing columns with NaN
    for col in expected_columns:
        if col not in df.columns:
            df[col] = None
    # Drop unexpected columns
    df = df[expected_columns]
    return df