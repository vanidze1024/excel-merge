import pandas as pd
import config_reader
from mapper import map_file

print('Чтение конфигурации...')
configs = config_reader.read_xls('config.xlsx')

print('Обработка файлов...')
output_data = pd.concat(map_file(path=config.path,
                                 sheet=config.sheet,
                                 skip_rows=config.skipRows,
                                 map_config=config.drop(['path', 'sheet', 'skipRows']).to_dict())
                        for (index, config) in configs.iterrows())

output_name = 'output.csv'
print(f'Сохранение данных в {output_name}...')
output_data.to_csv(output_name, index=False)
