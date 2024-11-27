from dataclasses import dataclass
import pandas as pd
#Mod
from original_request.reference_reg import sport_token

def receiving_messages(text:str):
	text = text.lower()
	df = sport_token()
	df_sersh = df[(df['token_name'].str.contains(fr"{text}", na=False))]
	df_sersh = df_sersh[['menu', 'correct_name']]
	df_sersh.drop_duplicates(inplace=True)
	df_sersh = df_sersh.reset_index(drop=True)
	return df_sersh


@dataclass
class SportClass:
    id_user: int
    text_user: str = None
    df: pd.DataFrame = None
