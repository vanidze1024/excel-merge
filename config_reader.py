import sys
import json
import re


def read(config_name: str) -> list:
    print('Проверка конфигурации...')

    try:
        with open(config_name, encoding='utf-8') as config_file:

            json_config = json.load(config_file)
            json_config = list([json_config]) if not isinstance(json_config, list) else json_config

            for config in json_config:
                _validate_config(config)

            _validate_map(json_config)

            return json_config
    except FileNotFoundError:
        sys.exit(f'Отсутствует файл {config_name}')
    except json.decoder.JSONDecodeError:
        sys.exit(f'Неверный формат данных в файле {config_name}')
    except Exception as e:
        sys.exit(e.args)


def _validate_config(config: dict):
    if 'path' not in config:
        raise Exception('В конфигурации отсутствует обязятельный параметр path')
    if not re.search(r'\.xls$|\.xlsx$', config['path'], re.IGNORECASE | re.VERBOSE):
        raise Exception('Поддерживаются только файлы формата *.xls и *.xlsx')
    if 'sheet' not in config:
        raise Exception('В конфигурации отсутствует обязятельный параметр sheet')
    if 'map' not in config or not isinstance(config['map'], dict):
        raise Exception('В конфигурации отсутствует обязятельный параметр map или он задан в неверном формате')


def _validate_map(configs: list):
    sets = list(map(lambda x: set(x['map'].keys()), configs))

    if len(sets) == 1:
        return

    for s in sets[1:]:
        if len(s.symmetric_difference(sets[0])) > 0:
            raise Exception('Колонки в "map" совпадают не у всех конфигураций')
