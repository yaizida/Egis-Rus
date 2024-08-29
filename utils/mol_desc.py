def mol_desc(value):
    if isinstance(value, str) and value:
        mol_table = dict()
        mol_descs = value.split('+')
        for i in range(len(mol_descs)):
            mol_table['Mol_Desc'+str(i+1)] = mol_descs[i]

        result = " and ".join([f"{key} == '{value}'" for key, value in mol_table.items()])
        return result

    return '0'

    # return value


# print(mol_desc('CYANOCOBALAMIN'))
