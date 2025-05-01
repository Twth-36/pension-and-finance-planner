def geometric12th(percrate: float):
    # rate as %-value not 0._
    monthRate = (1 + percrate / 100) ** (1 / 12)
    monthPercRate = (monthRate - 1) * 100
    return monthPercRate
