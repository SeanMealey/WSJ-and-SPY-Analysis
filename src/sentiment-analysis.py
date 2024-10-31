from transformers import pipeline
import json
import sqlite3
from datetime import datetime

def main():
    name = '/Users/seanmealey/wsjTest/Scraping/articlesWSJ.db'
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

    pipe = pipeline("text-classification", model="ProsusAI/finbert",device=0)
    sentimentDict = pipe(headlines)
    # with open('/Users/seanmealey/wsjTest/ollama/llamaData.json') as json_file:
    #     sentimentDict = json.load(json_file)

    scoresDatetimes = []

    for index in range(len(datetimes)):
        entry = {
            "Score": sentimentDict[index],
            "Datetime": datetimes[index]
        }
        scoresDatetimes.append(entry)
        
    with open('scoresDatetimesSelectSectors.json', 'w') as file:
        json.dump(scoresDatetimes, file, indent=4)

    # Write results to a JSON file
    with open('sentiment_resultsSelectSectors.json', 'w') as file:
        json.dump(sentimentDict, file, indent=4)


if __name__=="__main__":
    main()

    