
def str_cut(str, lim):
    if (len(str) <= lim):
        return  str
    idx = str.rfind('\n', 0, lim)
    if idx < 0:
        return str[:lim]
    else:
        return str[:idx]
