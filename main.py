import sys
import pandas as pd
import json
import itertools
import string
import re


def column_name_generator():
    for t in itertools.chain(
            itertools.product(string.ascii_uppercase, repeat=1),
            itertools.product(string.ascii_uppercase, repeat=2)):
        yield ''.join(t)


def read_config(config_name):
    try:
        with open(config_name, encoding='utf-8') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        sys.exit(f'Отсутствует файл {config_name}')
    except json.decoder.JSONDecodeError:
        sys.exit(f'Неверный формат данных в файле {config_name}')


def compute_column_value(expression: str, data: pd.DataFrame) -> str:
    expr = re.compile('\{(\w+)\}')
    format_string = expr.sub('{}', expression)

    result = data[map(lambda x: x.group(1), expr.finditer(expression))]\
        .apply(lambda x: format_string.format(*x.fillna('').to_numpy()), axis=1)

    return result


def map_file(file_config):
    excel_data = pd.read_excel(file_config['path'],
                               skiprows=file_config['skipRows'],
                               header=None,
                               sheet_name=file_config['sheet'])

    excel_data = excel_data.rename(columns={x: y for x, y in zip(excel_data.columns, column_name_generator())})

    columns_map = file_config['map']
    result_data = pd.DataFrame(columns=columns_map.keys())

    for result_col in result_data:
        result_data[result_col] = compute_column_value(columns_map[result_col], excel_data)

    return result_data


configs = read_config('config.json')

result = pd.concat(map_file(config) for config in configs)

result.to_csv('output.csv', index=False)
