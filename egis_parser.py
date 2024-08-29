import os
from collections import defaultdict

import pandas as pd
from tqdm import tqdm

from utils.transform_cond_operator import transform_cond
from utils.check_value import chek_valid_value
from utils.pre_cond import pre_cond
from utils.extracts import extract_numbers
from utils.pars_string import pars_sku
from utils.mol_desc import mol_desc
from utils.dict_to_csv import to_csv
from utils.csv_or_xlsx import read_file
from utils.check_levels import (check_nfc_level, check_eph_level,
                                check_nec_level)

# NEW_MARKET_PATH = r"C:\Users\nikita.b\Desktop\Dev\Egis-RUS\data\New.xlsx" # noqa
# REF_PATH = r"C:\Users\nikita.b\Desktop\Dev\Egis-RUS\data\Ref.csv" # noqa
# FCC_PATH = r'C:\Users\nikita.b\Desktop\Dev\Egis-RUS\data\fcc_list.csv' # noqa

NEW_MARKET_PATH = r"\\mskrusqlik01.rus.ad.egisplc.com\QlikTech\BI_IMPORT\XLS4PBI\IN\New market definition template.xlsx"  # noqa
REF_PATH = r"\\mskrusqlik01.rus.ad.egisplc.com\QlikTech\IMS_ff\Reference.csv" # noqa
FCC_PATH = r"\\mskrusqlik01.rus.ad.egisplc.com\QlikTech\BI_IMPORT\IMS_ff\fcc_markets.csv" # noqa


def main(df_new_market, df_reference):
    zero_markets = []
    fcc_df = {}

    for market in tqdm(df_new_market['Market'].unique()):
        # Формируем индексы только нужноого маркета
        need_market_indexs = df_new_market.index[df_new_market['Market'] ==
                                                 market].tolist()

        # Фомируем дата фрейм для нужного маркета
        need_markets = df_new_market.iloc[list(need_market_indexs)]

        # Сбрасываем индексы что бы они были 0,1,2,3
        need_markets = need_markets.reset_index(drop=True)

        conditions = defaultdict(list)

        # Все поля для условий выбраны
        for index_market in range(len(need_markets)):
            # Здесь мы достаем значение столбцов построчно

            main_cond = need_markets.loc[index_market, :]['Include_Exclude']

            if (str(need_markets.loc[index_market, :]['ATC_Level'])) != 'nan':
                wholevel = 'WHO_' + str(int(need_markets.loc[index_market, :]['ATC_Level'])) # noqa
            else:
                wholevel = 0
            nfc_level = check_nfc_level(need_markets.loc[index_market, :]['NFC_Level']) # noqa
            eph_level = check_eph_level(need_markets.loc[index_market, :]['EphMRA_Level']) # noqa
            nec_level = check_nec_level(need_markets.loc[index_market, :]['NEC_Level']) # noqa

            atc_pre_cond = pre_cond(need_markets, index_market, 'ATC_condition') # noqa
            inn_pre_cond = pre_cond(need_markets, index_market, 'INN_condition') # noqa
            nfc_pre_cond = pre_cond(need_markets, index_market, 'NFC_condition') # noqa
            eph_pre_cond = pre_cond(need_markets, index_market, 'EphMRA_condition') # noqa
            nec_pre_cond = pre_cond(need_markets, index_market, 'NEC_condition') # noqa

            # conditions[wholevel].append(atc_pre_cond)

            atc_value = chek_valid_value(need_markets.loc[index_market, :]['ATC']) # noqa
            nfc_value = chek_valid_value(need_markets.loc[index_market, :]['NFC']) # noqa
            inn_value = chek_valid_value(need_markets.loc[index_market, :]['INN']) # noqa
            eph_value = chek_valid_value(need_markets.loc[index_market, :]['EphMRA']) # noqa
            nec_value = chek_valid_value(need_markets.loc[index_market, :]['NEC']) # noqa
            trade_value = chek_valid_value(need_markets.loc[index_market, :]['TradeName']) # noqa
            sku_value = chek_valid_value(need_markets.loc[index_market, 'SKU'])

            conditions[market].append([main_cond,
                                       wholevel, atc_pre_cond,
                                       atc_value, nfc_level,
                                       nfc_pre_cond, nfc_value,
                                       inn_pre_cond, inn_value,
                                       eph_level, eph_pre_cond,
                                       eph_value, nec_level,
                                       nec_pre_cond, nec_value,
                                       trade_value,
                                       sku_value])

        fcc_list = []

        for cond_row in range(len(need_markets)):
            (main_cond, wholevel, atc_pre_cond, atc_value, nfc_level,
             nfc_pre_cond, nfc_value, inn_pre_cond, inn_value,
             eph_level, eph_pre_cond, eph_value, nec_level,
            nec_pre_cond, nec_value, trade_value, sku_value) = [x for x in conditions[market][cond_row]] # noqa

            # Mol_Desc == INN
            inn_indexs = df_reference.query(mol_desc(inn_value)).index
            fcc_list.append(inn_indexs)

            if isinstance(sku_value, str):
                sku_indexs = df_reference.query(
                    f"Product == '{pars_sku(sku_value)['Product']}' and " +
                    f"Pack_Desc == '{pars_sku(sku_value)['Pack_Desc']}'").index
                fcc_list.append(sku_indexs)

            # TradeName == BrandEng
            trade_indexs = df_reference.query(f"BrandEng == '{trade_value}'").index # noqa
            fcc_list.append(trade_indexs)

            # Здесь высчитываются who который atc и nfc
            try:
                indexs = df_reference.query(f"{wholevel} {transform_cond(atc_pre_cond)} '{atc_value}' and " + # noqa
                                            f"{nfc_level} {transform_cond(nfc_pre_cond)} '{nfc_value}' and " + # noqa
                                            f"{eph_level} {transform_cond(eph_pre_cond)} '{eph_value}' and  " + # noqa
                                            f"{nec_level} {transform_cond(nec_pre_cond)} '{nec_value}'").index # noqa
            except Exception:
                indexs = []
            if main_cond == "+":
                fcc_list.append(indexs)

        final_list = []

        # Возвращаем единный список из индексов
        # final_list = sum((extract_numbers(item) for item in fcc_list), [])
        for item in fcc_list:
            final_list += extract_numbers(item)

        fcc_list = df_reference.loc[final_list, 'Fcc']

        # Проверка какие есть пусты поля
        if len(fcc_list) == 0:
            zero_markets.append(market)

        fcc_df[market] = fcc_list

    new_fcc_df = {}

    for market, fcc in tqdm(fcc_df.items()):
        new_fcc_df[market] = fcc.to_string(index=False, header=False).split('\n') # noqa

    print('Поля с нулевым значением: ', zero_markets)

    print('Формирую csv, подождите')

    to_csv(new_fcc_df, FCC_PATH)

    file_fcc_df =  read_file(FCC_PATH) # noqa

    market_list = [market for market in file_fcc_df.keys()]
    df_list = []

    print('Переформировываю в нужный формат ваш файл')

    for market in tqdm(market_list):
        new_df = pd.DataFrame({
                              'Brand': [],
                              'Fcc': [],
                              'Core': [],
                              })
        fcc_list = []
        for value in file_fcc_df[market]:
            if str(value) == 'nan':
                break
            fcc_list.append(int(value))

        new_df['Brand'] = [market for _ in range(len(fcc_list))]
        new_df['Fcc'] = fcc_list

        for row in df_new_market.values.tolist():
            if list(row)[0] == market:
                core_value = row[1]
                break
        new_df['Core'] = core_value

        df_list.append(new_df)

    df = pd.concat(df_list).reset_index(drop=True).drop_duplicates()

    if os.path.exists(FCC_PATH):
        # Если файл существует, удаляем егоs
        os.remove(FCC_PATH)

    df.to_csv(FCC_PATH, index=False, header=True)


if __name__ == '__main__':
    file_markets = NEW_MARKET_PATH # noqa
    file_ref = REF_PATH # noqa

    print('Извините, файлы слишком большие\n' +
          'Их чтение может занять какое то время\n' +
          'После прочтения программой файлов, начнётся загрузка')

    main(read_file(file_markets), read_file(file_ref))
