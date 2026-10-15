from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import mysql.connector
from app.database import db_transaction
class ScraperService:
    @staticmethod
    def scrape_books_to_scrape():
        base='https://books.toscrape.com/'
        response=requests.get(base,timeout=10,headers={'User-Agent':'RiskLens portfolio practice scraper/1.0'})
        response.raise_for_status()
        soup=BeautifulSoup(response.text,'html.parser')
        records=[]; skipped=0
        with db_transaction() as (_,c):
            for book in soup.select('article.product_pod'):
                anchor=book.select_one('h3 a'); price=book.select_one('p.price_color'); rating=book.select_one('p.star-rating')
                if not (anchor and price and rating): continue
                title=anchor.get('title','').strip(); url=urljoin(base,anchor.get('href',''))
                classes=rating.get('class',[]); stars=next((v for v in classes if v!='star-rating'),'Unrated')
                try:
                    c.execute('INSERT INTO scraped_books (title,price,rating,product_url) VALUES (%s,%s,%s,%s)',(title,price.get_text(strip=True),stars,url))
                    records.append({'id':c.lastrowid,'title':title,'price':price.get_text(strip=True),'rating':stars,'product_url':url})
                except mysql.connector.IntegrityError as e:
                    if e.errno==mysql.connector.errorcode.ER_DUP_ENTRY: skipped+=1
                    else: raise
        return {'message':'Practice books saved to scraped_books table.','new_records_inserted':len(records),'duplicates_skipped':skipped,'records':records}
