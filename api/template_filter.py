import time


def formatted_time(timestamp):
    t = timestamp
    format = '%Y/%m/%d %H:%M'
    t = time.localtime(timestamp)
    ft = time.strftime(format, t)
    return ft
