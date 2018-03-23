# -*- coding: utf-8 -*-

from datetime import date, datetime

def parse_date(date_str):
    "Parses a date string of the format YYYY-MM-DD"
    return datetime.strptime(date_str, '%Y-%m-%d')

def parse_datetime(datetime_str):
    "Parses a datetime string of the format YYYY-MM-DD HH:MM:SS"
    return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
