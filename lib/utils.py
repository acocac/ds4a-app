from datetime import datetime

def parse_dates(year, month):
    start_date = f'20{year[0]:02}-{month[0]:02}'
    startPeriod = datetime.strptime(start_date, '%Y-%m')
    end_date = f'20{year[1]:02}-{month[1]:02}'
    endPeriod = datetime.strptime(end_date, '%Y-%m')
    return startPeriod, endPeriod