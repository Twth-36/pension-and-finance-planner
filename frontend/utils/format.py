def formatswiss(value: float, decimals: int = 0):
    if value is None:
        return "n.a."
    return f"{value:,.{decimals}f}".replace(",", "'")
