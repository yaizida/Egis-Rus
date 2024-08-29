def pre_cond(need_markets, index_market, value):
    try:
        return int(need_markets.loc[index_market, :][value])
    except Exception:
        return 0

