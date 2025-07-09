import pandas as pd

def save_table_to_excel(table: list, filename: str) -> str:
    df = pd.DataFrame(table[1:], columns=table[0]) if len(table) > 1 else pd.DataFrame(table)
    df.to_excel(filename, index=False)
    return filename
