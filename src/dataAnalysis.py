import json
import sqlite3
from datetime import datetime
import sys


name = 'articlesWSJ.db'
conn = sqlite3.connect(name)

c = conn.cursor()
c.execute(''' SELECT id,headline,year,month,day FROM articles_index ''')

articleRecords = c.fetchall()

headlinesAndDatetimes = []
headlines = []

for i in articleRecords:
    date_string = f"{i[2]}-{i[3]}-{i[4]}"
    headline = i[1]
    entry = [headline,date_string]
    headlines.append(headline)
    headlinesAndDatetimes.append(entry)

with open('/Users/seanmealey/wsjTest/ollama/llamaData.json', 'r') as file:
    data = json.load(file)



count = 0

with open('/Users/seanmealey/wsjTest/ollama/llamaHeadlineScores.txt', 'w') as f:
    original_stdout = sys.stdout  
    sys.stdout = f  

    for entry in data:
        score = entry.get('Score')
        
        print(f"Score: {score}")
        if count<len(headlines):
            print("Headline: ", headlines[count])
        else:
            print("N/A")
        print("")
        count += 1

sys.stdout = original_stdout  
