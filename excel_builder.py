from openpyxl import Workbook

def save_table_to_excel(table: list[list[str]], path: str) -> str:
    wb = Workbook()
    ws = wb.active
    for row in table:
        ws.append(row)
    wb.save(path)
    return path
