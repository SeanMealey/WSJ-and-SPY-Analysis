import sqlite3

def main():
    name = 'extraDataArticlesWSJ.db'
    conn = sqlite3.connect(name)

    c = conn.cursor()

    # Table "articles_index"
    c.execute('''CREATE TABLE IF NOT EXISTS articles_index (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            
            year TEXT, 
            month TEXT, 
            day TEXT, 
            
            headline TEXT, 
            article_time TEXT,
            
            keyword TEXT,
            link TEXT, 
            
            scraped_at TEXT,
            scanned_status INTEGER)''')


    conn.commit()
    conn.close()

    print("DB and tables created")

if __name__ == "__main__":
    main()