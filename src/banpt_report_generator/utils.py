# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
from . import constants

def parse_date(date_str):
    "Parses a date string of the format YYYY-MM-DD"
    return datetime.strptime(date_str, '%Y-%m-%d')

def parse_datetime(datetime_str):
    "Parses a datetime string of the format YYYY-MM-DD HH:MM:SS"
    return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

def n_mins_before_now(n):
    return datetime.now() - timedelta(minutes=n)

def calculate_ts_year(year, report_year):
    if year - report_year > 0:
        return 'TS+' + str(year - report_year)
    if year - report_year < 0:
        return 'TS-' + str(report_year - year)
    return 'TS'

def get_year(date_str):
    return parse_date(date_str).year

def get_nim_year(nim_str):
    nim = int(nim_str[3:5])
    return nim + (2000 if nim < 70 else 1900)

def nim_type(nim_str):
    nim_last_digits = nim_str[-3:]
    if int(nim_last_digits) >= constants.TRANSFER_STUDENT_NIM_START and int(nim_last_digits) <= constants.TRANSFER_STUDENT_NIM_END:
        return constants.TRANSFER_STUDENT
    if int(nim_last_digits) >= constants.NONREGULAR_STUDENT_NIM_START and int(nim_last_digits) <= constants.NONREGULAR_STUDENT_NIM_END:
        return constants.NONREGULAR_STUDENT
    return constants.REGULAR_STUDENT
