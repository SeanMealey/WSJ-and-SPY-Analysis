import json
from datetime import datetime, timedelta
from re import S

def isFriday(date_string):
    date_object = datetime.strptime(date_string, "%Y-%m-%d")
    day_of_week = date_object.weekday()
    
    return day_of_week == 4

def isWeekday(date_string):
    date_object = datetime.strptime(date_string, "%Y-%m-%d")
    day_of_week = date_object.weekday()
    
    return day_of_week < 5
def calculate_good_friday(year):
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    easter_date = datetime(year, month, day)
    good_friday = easter_date - timedelta(days=2)
    return good_friday

def isFederalHoliday(date_str):
    date = datetime.strptime(date_str, '%Y-%m-%d')
    year = date.year
    holidays = {
        (1, 1): "New Year's Day",
        (7, 4): "Independence Day",
        (12, 25): "Christmas Day",
    }
    for month_day, name in holidays.items():
        month, day = month_day
        holiday_date = datetime(year, month, day)
        if holiday_date.weekday() == 5:
            holiday_date = holiday_date - timedelta(days=1)
        elif holiday_date.weekday() == 6:
            holiday_date = holiday_date + timedelta(days=1)
        if date == holiday_date:
            return True
    if date.month == 1 and date.weekday() == 0 and 15 <= date.day <= 21:
        return True
    if date.month == 2 and date.weekday() == 0 and 15 <= date.day <= 21:
        return True
    if date.month == 5 and date.weekday() == 0 and date.day >= 25:
        return True
    if date.month == 9 and date.weekday() == 0 and date.day <= 7:
        return True
    if date.month == 11 and date.weekday() == 3 and 22 <= date.day <= 28:
        return True
    if date == calculate_good_friday(year):
        return True
    return False


def main():
    pathTojson = 'llama-scoresDatetimesSelectSectors.json';
    with open(pathTojson, 'r') as file:
        data = json.load(file)
    
    aggregateDayScores = []
    prevDay = data[1]['Datetime']
    daySum = 0
    aggregateScore = 0
    for i in data:
        if i['Datetime']==prevDay:
            aggregateScore += float(i['Score']['Score'])
        else:
            entry = [aggregateScore,i['Datetime']]
            aggregateDayScores.append(entry)
            aggregateScore = 0
        prevDay = i['Datetime']

    scores = []

    for i in range(2,len(aggregateDayScores)-2):
        if isFriday(aggregateDayScores[i][1]) and i!=len(aggregateDayScores):
            friScore = (aggregateDayScores[i][0] + aggregateDayScores[i+1][0]+aggregateDayScores[i+2][0])/3
            scores.append(friScore)
            i += 2
        else:
            scores.append(aggregateDayScores[i][0])

    pathToFile = '/Users/seanmealey/wsjTest/src/outputV3-SelectSectors.txt'

    with open(pathToFile, 'w') as file:
        for i in aggregateDayScores:
            if isWeekday(i[1]) and not isFederalHoliday(i[1]):
                line = f"{i[0]},{i[1]}\n"
                file.write(line)
        
if __name__ == "__main__":
    main()
        