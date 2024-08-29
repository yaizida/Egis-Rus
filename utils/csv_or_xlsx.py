import chardet

import pandas as pd


def read_file(file_path):
    """
    Читает файл CSV или Excel в DataFrame.

    Args:
        file_path: Путь к файлу.

    Returns:
        DataFrame, если файл успешно прочитан, иначе None.
    """
    if file_path.lower().endswith('.xlsx'):
        # with open(file_path, 'rb') as f:
        #     result = chardet.detect(f.read())
        #     encoding = result['encoding']
        return pd.read_excel(file_path)

    elif file_path.lower().endswith('.csv'):
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
            encoding = result['encoding']
        return pd.read_csv(file_path, encoding=encoding)

    else:
        print(f"Неподдерживаемый формат файла: {file_path}")
        return None
