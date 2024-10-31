import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import sqlite3
import time
from datetime import datetime, timedelta

class ManagementDB():
    def __init__(self, db_name='articlesWSJ.db'):
        self.name = db_name
        try:
            self.conn = sqlite3.connect(self.name)
        except sqlite3.Error as e:
            print(f"Database connection failed: {e}")
            self.conn = None
        self.c = self.conn.cursor() if self.conn else None

    def insert_elements(self, elements):
        if not self.c:
            print("No valid database connection to insert elements.")
            return
        try:
            self.c.execute("INSERT INTO articles_index (headline, article_time, year, month, day, keyword, link, scraped_at, scanned_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (elements["headline"], elements["article_time"], elements["year"], elements["month"], elements["day"], elements["keyword"],
                   elements["link"], elements["scraped_at"], elements["scanned_status"]))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def exploration(self, link, day, month, year, page_num, values_or_not, count_articles):
        if not self.c:
            print("No valid database connection to perform exploration.")
            return
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
            self.c.execute(''' INSERT INTO exploration (link, day, month, year, page_num, checked_at, values_or_not, count_articles)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (link, day, month, year, page_num, current_time, values_or_not, count_articles))
    
            self.conn.commit()
        
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        
    def closeDB(self):
        if self.conn:
            self.conn.close()

class WebScrap:
    def __init__(self):
        self.page_number = 1
        self.total_articles = 0
        
    def reset(self):
        self.page_number = 1
        self.total_articles = 0
        
    def _save_to_json(self, article_details, year, month, day):
        title_json = f"article_titles_json/index_{year}_{month}_{day}_page_{self.page_number}.json"
        try:
            with open(title_json, 'w') as f:
                json.dump(article_details, f)
            print(f'Article details saved to {title_json}')
        except IOError as e:
            print(f"Failed to save articles to JSON: {e}")

    def get_elements_from_web(self, year, month, day, waiting_time):

        db = ManagementDB()
        if not db.conn:
            print("Cannot proceed without a valid database connection.")
            return

        end_page = False
        
        while not end_page:
            
            title_url = f'https://www.wsj.com/news/archive/{year}/{month}/{day}?page={self.page_number}'
            print(title_url)
    
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0 '}
            try:
                page = requests.get(title_url, headers=headers)
            except requests.RequestException as e:
                print(f"Request failed: {e}")
                return
            
            article_details = []

            if page.status_code == 200:
                soup = BeautifulSoup(page.content, 'html.parser')
                print('Page status code:', page.status_code)

                ol_element = soup.find('ol', class_='WSJTheme--list-reset--3pR-r52l')
        
                if ol_element:
                    article_elements = ol_element.find_all('article')
            
                    if not article_elements:

                        db.exploration(title_url, day, month, year, self.page_number, 0, 0)
                        end_page = True
                        self.reset()
                        
                    else:
                        count_articles = 0
                        for article in article_elements:
                            headline_span = article.find('span', class_='WSJTheme--headlineText--He1ANr9C')
                            a_tag = article.find('a')
                            timestamp_p = article.find('p', class_='WSJTheme--timestamp--22sfkNDv')

                            headline_text = headline_span.text if headline_span else "N/A"
                            article_link = a_tag['href'] if a_tag else "N/A"
                            article_time = timestamp_p.text if timestamp_p else "N/A"

                            article_type_div = article.find('div', class_='WSJTheme--articleType--34Gt-vdG')
                            empty_class_span = None

                            if article_type_div:
                                empty_class_span = article_type_div.find('span', class_='')

                            article_type_text = empty_class_span.text if empty_class_span else "N/A"

                            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
                            dict_elements = {
                                'headline': headline_text,
                                'article_time': article_time,
                
                                'year' : year,
                                'month' : month,
                                'day' : day,
                
                                'keyword': article_type_text,
                                'link': article_link,
                
                                'scraped_at': current_time,
                                'scanned_status':0,
                            }

                            article_details.append(dict_elements)

                            db.insert_elements(dict_elements)
                    
                            count_articles += 1
                       
                        
                        self._save_to_json(article_details, year, month, day)

                        db.exploration(title_url, day, month, year, self.page_number, 1, count_articles) #Page explored
                        self.total_articles = self.total_articles + count_articles
                        
                        if count_articles == 50:
                            self.page_number +=1
                            time.sleep(waiting_time)
                        else:
                            print(f'Articles in the day {self.total_articles}')
                            end_page = True
                            self.reset()
                        
                else:
                    print("Could not find <ol> element with the specified class.")
                    end_page = True
                    self.reset()

            else:
                print(f"Failed to retrieve the page. Status code: {page.status_code}")
                end_page = True
                self.reset()
        
        db.closeDB()
        
def get_dates(year):
    start_date = datetime(2022, 11, 11)
    end_date = datetime(2024, 10, 20)
    date_list = []
    
    current_date = start_date
    while current_date <= end_date:
        date_list.append([current_date.day, current_date.month, current_date.year])
        current_date += timedelta(days=1)
    
    return(date_list)
    

def searching(year, waiting_time):
    try:
        dates = get_dates(year)
        scrap = WebScrap()
        for day, month, year in dates:
            print(day, month, year)
            scrap.get_elements_from_web(year, month, day, waiting_time)
            time.sleep(waiting_time)
    except Exception as e:
        print(f"An error occurred during searching: {e}")

def main():
    try:
        year = 2020
        waiting_time = 7

        searching(year, waiting_time)
    except Exception as e:
        print(f"An error occurred in the main execution: {e}")

    print("end")

if __name__ == '__main__':
    main()
    