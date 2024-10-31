from asyncore import write
from transformers import pipeline
import json
import sqlite3
from datetime import datetime

def main():
    name = 'articlesWSJ.db'
    conn = sqlite3.connect(name)

    c = conn.cursor()
    c.execute(''' SELECT id,headline,year,month,day FROM articles_index ''')

    articleRecords = c.fetchall()

    headlinesAndDatetimes = []
    headlines = []
    datetimes = []

    for i in articleRecords:
        date_string = f"{i[2]}-{i[3]}-{i[4]}"
        headline = i[1]
        entry = [headline,date_string]
        datetimes.append(date_string)
        headlines.append(headline)
        headlinesAndDatetimes.append(entry)
        
    f = open("headlinesV2.txt", "a")
    for i in headlines:
        f.write(f"{i}\n")
    f.close()

if __name__ == '__main__':
    main()