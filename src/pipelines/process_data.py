import pandas as pd
import re
from typing import List, Tuple, Optional

def process_data(
        data_path: str,
        string_columns: Optional[List[str]] = None,
        numeric_columns: Optional[List[str]] = None,
        date_columns: Optional[List[str]] = None,
        duration_columns: Optional[Tuple[str, str, str]] = None,
        required_columns: Optional[List[str]] = None,
        string_transform: str = 'title',
        on_bad_lines: str = 'skip'
) -> pd.DataFrame:
    """Process a CSV DataFrame with minimal loops using vectorized operations."""
    # Charger CSV et normaliser les noms de colonnes
    df = pd.read_csv(data_path, on_bad_lines=on_bad_lines)
    df.columns = [re.sub(r"[ .-]+", "_", c.strip().lower()) for c in df.columns]

    # Détection automatique des types si non spécifiés
    string_columns = string_columns or df.select_dtypes('object').columns.tolist()
    numeric_columns = numeric_columns or df.select_dtypes(['int64', 'float64']).columns.tolist()
    date_columns = date_columns or [col for col in df.columns if 'date' in col.lower()]

    # Transformations vectorisées pour les chaînes
    if string_columns:
        transform = getattr(str, string_transform, str.title)
        str_cols = [col for col in string_columns if col in df.columns]
        df[str_cols] = df[str_cols].apply(
            lambda s: s.str.replace('"', '', regex=False)
                      .str.replace(r'\s+', ' ', regex=True)  # Remplacer espaces multiples
                      .str.strip()
                      .apply(lambda x: transform(x) if isinstance(x, str) else x)
        )

    # Conversions vectorisées pour les numériques et dates
    if numeric_columns:
        num_cols = [col for col in numeric_columns if col in df.columns]
        df[num_cols] = df[num_cols].apply(pd.to_numeric, errors='coerce')
    if date_columns:
        date_cols = [col for col in date_columns if col in df.columns]
        df[date_cols] = df[date_cols].apply(pd.to_datetime, errors='coerce')

    # Calcul de la durée
    if duration_columns and duration_columns[0] in df.columns and duration_columns[1] in df.columns:
        df[duration_columns[2]] = (df[duration_columns[1]] - df[duration_columns[0]]).dt.days

    # Suppression des NaN dans les colonnes requises
    if required_columns:
        df = df.dropna(subset=[col for col in required_columns if col in df.columns])

    return df



