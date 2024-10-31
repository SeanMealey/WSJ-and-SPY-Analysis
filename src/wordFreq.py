from collections import defaultdict
import sqlite3
from datetime import datetime
import os

def get_word_frequency(strings):
    # Create a defaultdict to hold word frequencies
    word_frequency = defaultdict(int)

    # Iterate over each string in the list
    for string in strings:
        # Split the string into words based on spaces
        words = string.split()

        # Iterate over each word in the current string
        for word in words:
            # Normalize the word to lowercase to make counting case-insensitive
            word = word.lower()
            # Increment the word's frequency
            word_frequency[word] += 1

    return word_frequency

def main():
    conn = sqlite3.connect('articlesWSJ.db')

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


    frequencies = get_word_frequency(headlines)
    sorted_by_values = dict(sorted(frequencies.items(), key=lambda item: item[1]))

    for word, count in sorted_by_values.items():
        print(f"'{word}': {count}")

if __name__=="__main__":
    main()