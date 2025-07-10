import pandas as pd
import os

def save_to_excel(table_data: list[list[str]], file_id: str) -> str:
    df = pd.DataFrame(table_data)
    output_path = f"temp/{file_id}.xlsx"
    os.makedirs("temp", exist_ok=True)
    df.to_excel(output_path, index=False, header=False)
    return output_path
