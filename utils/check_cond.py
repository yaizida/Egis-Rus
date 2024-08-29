def check_condition(value):
    if str(value) == '1.0':
        return True
    elif str(value) == 'nan':
        return False
    return False
