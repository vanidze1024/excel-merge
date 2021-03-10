import openpyxl
import xlrd
import pandas as pd
from tools import column_name_generator
from column_parser import compute_column_value


def map_file(path: str, sheet: str, skip_rows: str, map_config: dict) -> pd.DataFrame:
    print(f'Обработка {path} -> {sheet}...')
    excel_data = pd.read_excel(path,
                               skiprows=skip_rows,
                               sheet_name=sheet,
                               header=None,
                               engine=None)

    excel_data = excel_data.rename(columns={x: y for x, y in zip(excel_data.columns, column_name_generator())})

    result_data = pd.DataFrame(columns=map_config.keys())

    for result_col in result_data:
        result_data[result_col] = compute_column_value(map_config[result_col], excel_data)

    return result_data
