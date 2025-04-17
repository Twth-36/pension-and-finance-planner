def formatswiss(value: float, decimals: int = 0):
    return f"{value:,.{decimals}f}".replace(",", "'")
