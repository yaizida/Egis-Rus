def check_nfc_level(value):
    if str(value) != 'nan':
        nfc = 'NFC_'
        try:
            for level in range(1, (int(value)+1)):
                nfc += str(level)
            return nfc
        except Exception:
            return 0
    return 0


def check_eph_level(value):
    if str(value) != 'nan':
        return 'ATC_' + str(int(value))
    return 0


def check_nec_level(value):
    if str(value) != 'nan':
        return 'CHC_NEC_Code' + str(int(value))
    return 0
