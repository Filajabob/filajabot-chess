def smart_round(x, digits):
    try:
        return round(x, digits)
    except TypeError:
        return x