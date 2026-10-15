import os
import unittest
from unittest.mock import patch, Mock
from app import create_app
from app.database import get_db_connection

HTML='<article class="product_pod"><p class="star-rating Three"></p><h3><a title="Test Book" href="catalogue/test_1/index.html">Test Book</a></h3><p class="price_color">£12.00</p></article>'

class RiskLensTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app=create_app(); cls.app.config['TESTING']=True
        cls.client=cls.app.test_client()

    def setUp(self):
        with self.app.app_context():
            conn=get_db_connection(); c=conn.cursor()
            try:
                c.execute('SELECT DATABASE()')
                if c.fetchone()[0] != 'risklens_test_db': raise RuntimeError('Refusing destructive test cleanup outside risklens_test_db')
                c.execute('DELETE FROM businesses'); c.execute('DELETE FROM scraped_books'); conn.commit()
            finally: c.close(); conn.close()

    def test_health(self):
        self.assertEqual(self.client.get('/api/health').status_code,200)

    def test_crud_risk_and_duplicate(self):
        b={'company_name':'Test Corp','registration_number':'T-001','country':'India','industry':'Software','contact_email':'test@example.com','founded_year':2020}
        r=self.client.post('/api/businesses',json=b); self.assertEqual(r.status_code,201)
        id=r.json['data']['id']
        self.assertEqual(self.client.post('/api/businesses',json=b).status_code,400)
        self.assertEqual(self.client.get(f'/api/businesses/{id}').status_code,200)
        self.assertEqual(self.client.get(f'/api/risk/evaluate/{id}').status_code,200)
        self.assertEqual(self.client.put(f'/api/businesses/{id}',json={'industry':'Finance'}).status_code,200)
        self.assertEqual(self.client.delete(f'/api/businesses/{id}').status_code,200)
        self.assertEqual(self.client.get(f'/api/businesses/{id}').status_code,404)

    def test_validation(self):
        self.assertEqual(self.client.post('/api/businesses',data='bad',content_type='application/json').status_code,400)
        self.assertEqual(self.client.post('/api/businesses',json={'company_name':'X','registration_number':'Y','country':'India','contact_email':'bad'}).status_code,400)
        self.assertEqual(self.client.get('/api/businesses?page=0').status_code,400)
        self.assertEqual(self.client.get('/api/businesses?limit=500').status_code,400)

    @patch('app.services.scraper_service.requests.get')
    def test_scraper(self,get):
        get.return_value=Mock(text=HTML,status_code=200)
        r=self.client.post('/api/scrape/practice-site'); self.assertEqual(r.status_code,201); self.assertEqual(r.json['new_records_inserted'],1)
        r=self.client.post('/api/scrape/practice-site'); self.assertEqual(r.json['duplicates_skipped'],1)

if __name__=='__main__': unittest.main()
