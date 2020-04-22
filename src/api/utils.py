from datetime import datetime as dt


def nowstr():
    return dt.now().strftime('%Y%m%d %H:%M:%S.%f')
