def pars_sku(sku) -> list:
    """
    :param sku:
    :return:
    """
    if isinstance(sku, str):
        sku_list = sku.split('_')
        if len(sku_list) == 2:
            return {'Product': sku_list[0], 'Pack_Desc': sku_list[1]}
        return {'Product': sku_list[0], 'Pack_Desc': 0}
    return 0
