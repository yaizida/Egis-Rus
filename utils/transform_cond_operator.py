def transform_cond(value):
    if value == 1:
        return '=='
    elif value == 0:
        return '!='
    else:
        return '0'
