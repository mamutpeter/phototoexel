import pandas as pd

def save_table_to_excel(table_data: list, file_path: str) -> str:
    df = pd.DataFrame(table_data)
    df.to_excel(file_path, index=False)
    return file_path
