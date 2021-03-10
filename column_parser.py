import re
import pandas as pd


def compute_column_value(expression: str, data: pd.DataFrame):
    expr = re.compile(r'\{(\w+)\}')
    format_string = expr.sub('{}', expression)

    result = data[map(lambda x: x.group(1), expr.finditer(expression))] \
        .apply(lambda x: format_string.format(*x.fillna('').to_numpy()), axis=1)

    return result
