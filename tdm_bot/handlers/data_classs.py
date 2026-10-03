from dataclasses import dataclass
import pandas as pd

@dataclass
class SportClass:
    """Класс для хранения результатов поиска"""
    id_user: int
    df: pd.DataFrame
    text_user: str
