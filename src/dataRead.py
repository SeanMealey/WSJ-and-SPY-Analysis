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
    pathTojson = 'scoresDatetimesSelectSectors.json';
    with open(pathTojson, 'r') as file:
        data = json.load(file)


    aggregateDayScores = []
    prevDay = data[1]['Datetime']
    daySum = 0
    positiveScore = 0
    negativeScore = 0
    neutralScore = 0
    for i in data:
        if i['Datetime']==prevDay:
            if i['Score']['label'] == 'positive':
                positiveScore += i['Score']['score']
            elif i['Score']['label'] == 'negative':
                negativeScore += i['Score']['score']
            elif i['Score']['label'] == 'neutral':
                neutralScore += i['Score']['score']
        else:
            entry = [positiveScore,negativeScore,neutralScore,i['Datetime']]
            aggregateDayScores.append(entry)
            positiveScore = 0
            negativeScore = 0
            neutralScore = 0
        prevDay = i['Datetime']

    lastItem = aggregateDayScores[0]
    positiveScores = []
    negativeScores = []
    neutralScores = []
    for i in range(2,len(aggregateDayScores)-2):
        if isFriday(aggregateDayScores[i][3]) and i!=len(aggregateDayScores):
            posFriScore = (aggregateDayScores[i][0] + aggregateDayScores[i+1][0]+aggregateDayScores[i+2][0])/3
            negFriScore = (aggregateDayScores[i][1] + aggregateDayScores[i+1][1]+aggregateDayScores[i+2][1])/3
            neutralFriScore = (aggregateDayScores[i][2] + aggregateDayScores[i+1][2]+aggregateDayScores[i+2][2])/3
            
            positiveScores.append(aggregateDayScores[i][0])
            negativeScores.append(aggregateDayScores[i][1])
            neutralScores.append(aggregateDayScores[i][2])
            
            i += 2
        else:
            positiveScores.append(aggregateDayScores[i][0])
            negativeScores.append(aggregateDayScores[i][1])
            neutralScores.append(aggregateDayScores[i][2])

    pathToFile = 'output.txt'

    with open(pathToFile, 'w') as file:
        for i in aggregateDayScores:
            if isWeekday(i[3]) and not isFederalHoliday(i[3]):
                line = f"{i[0]},{i[1]},{i[2]},{i[3]}\n"
                file.write(line)
            
            
if __name__ == '__main__':
    main()