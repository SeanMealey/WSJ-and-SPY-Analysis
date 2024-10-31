import sqlite3

def main():
    name = '/Users/seanmealey/wsjTest/Scraping/articlesWSJ.db'
    conn = sqlite3.connect(name)
    cursor = conn.cursor()

    keywords_to_delete = [
        'Bookshelf',
        'Health',
        'Obituaries',
        'Fashion',
        'Crossword',
        'Television Review',
        'Essay',
        'Olympics',
        'Film Review',
        'Jason Gay',
        'The A-Hed',
        'NFL',
        'Sports',
        'MLB',
        'Music Review',
        'Food & Drink',
        'Off Duty Travel',
        'Design',
        'Art Review',
        'Magazine - Culture',
        'Soccer',
        'Health & Wellness',
        'NBA',
        'Culture',
        'House Call',
        'Icons',
        'Arts & Entertainment',
        'Music',
        'Television',
        'Travel',
        'Recipes',
        'Tennis',
        'Crossword Contest',
        'On Wine',
        'College Basketball',
        'Golf',
        'Screen Time',
        'Film',
        'Art & Design',
        'Off Brand',
        'Moving Targets',
        'Opera Review',
        'Variety Puzzle',
        'Art & Auctions',
        'Journal Reports: College Rankings',
        'Art',
        'Anatomy of a Workout',
        'What\'s Your Workout?',
        'ON TREND',
        'Dance Review',
        'Food',
        'NHL',
        'Obituary',
        'Books',
        'Acrostic',
        'Wilczek\'s Universe',
        'Anatomy of a Song',
        'A-hed',
        'Soapbox',
        'In My Kitchen',
        'Auto Racing',
        'Fitness',
        'A-Hed',
        'Comfort Reads',
        'inside story',
        'jason Gay'
    ]

    placeholders = ', '.join('?' for _ in keywords_to_delete)
    delete_statement = f'''
    DELETE FROM articles_index
    WHERE keyword IN ({placeholders});
    '''

    try:
        cursor.execute(delete_statement, keywords_to_delete)
        conn.commit()

        print("Rows deleted successfully.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        conn.close()
        
if __name__=="__main__":
    main()