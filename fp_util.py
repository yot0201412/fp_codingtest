import datetime

def scrap_line(line):
    date_str, ip, status = line.rstrip("\n").split(",")
    return str_to_date(date_str), ip, status

def is_error_status(status):
    return status == "-"

def str_to_date(date_str):
    return datetime.datetime.strptime(date_str, '%Y%m%d%H%M%S')