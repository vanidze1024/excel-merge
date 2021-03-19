import re
import openpyxl
import xlrd
import pandas as pd


def read_xls(path: str) -> pd.DataFrame:
    print('Проверка конфигурации...')
    config_data = pd.read_excel(path,
                                header=None,
                                engine=None)

    config_data_transposed = config_data.drop([0], axis=1).T
    config_data_transposed = config_data_transposed.rename(columns={x: y for x, y in zip(config_data_transposed.columns,
                                                                                         config_data[0])})
    config_data_transposed.apply(_validate_config, axis=1)
    return config_data_transposed


def _validate_config(config: pd.Series):
    if not hasattr(config, 'path'):
        raise Exception('В конфигурации отсутствует обязятельный параметр path')
    if not re.search(r'\.xls$|\.xlsx$', config.path, re.IGNORECASE | re.VERBOSE):
        raise Exception('Поддерживаются только файлы формата *.xls и *.xlsx')
    if not hasattr(config, 'sheet'):
        raise Exception('В конфигурации отсутствует обязятельный параметр sheet')
