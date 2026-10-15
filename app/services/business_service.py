import re
from datetime import datetime
import mysql.connector
from app.database import db_transaction, get_db_connection

FIELDS=('company_name','registration_number','country','industry','contact_email','founded_year')
class BusinessService:
    @staticmethod
    def validate_business_data(data, is_update=False):
        if not isinstance(data,dict): raise ValueError('Request body must be a JSON object.')
        if not is_update:
            for field in FIELDS[:3]:
                if field not in data: raise ValueError(f'Missing required field: {field}.')
        for field in FIELDS[:3]:
            if field in data and (not isinstance(data[field],str) or not data[field].strip()):
                raise ValueError(f'{field} must be a non-empty string.')
        for field in ('industry','contact_email'):
            if field in data and data[field] is not None and not isinstance(data[field],str):
                raise ValueError(f'{field} must be a string or null.')
        email=data.get('contact_email')
        if email is not None and (not email.strip() or not re.fullmatch(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}',email.strip())):
            raise ValueError('Invalid email format.')
        year=data.get('founded_year')
        if year is not None and (type(year) is not int or not 1800 <= year <= datetime.now().year):
            raise ValueError('founded_year must be an integer between 1800 and the current year.')

    @staticmethod
    def create_business(data):
        BusinessService.validate_business_data(data)
        vals=[data.get(f) for f in FIELDS]
        vals=[v.strip() if isinstance(v,str) else v for v in vals]
        try:
            with db_transaction() as (_,c):
                c.execute('INSERT INTO businesses (company_name,registration_number,country,industry,contact_email,founded_year) VALUES (%s,%s,%s,%s,%s,%s)',tuple(vals))
                c.execute('SELECT * FROM businesses WHERE id=%s',(c.lastrowid,))
                return c.fetchone()
        except mysql.connector.IntegrityError as e:
            if e.errno == mysql.connector.errorcode.ER_DUP_ENTRY: raise ValueError('A business with this registration number already exists.') from e
            raise

    @staticmethod
    def get_business_by_id(business_id):
        conn=get_db_connection(); c=None
        try:
            c=conn.cursor(dictionary=True); c.execute('SELECT * FROM businesses WHERE id=%s',(business_id,)); return c.fetchone()
        finally:
            if c: c.close()
            conn.close()

    @staticmethod
    def get_all_businesses(filters,page,limit):
        try:
            if str(page).strip()!=str(int(page)) or str(limit).strip()!=str(int(limit)): raise ValueError()
            page=int(page); limit=int(limit)
        except (ValueError,TypeError): raise ValueError('Page and limit must be integers.')
        if page<1 or not 1<=limit<=100: raise ValueError('Page must be >= 1 and limit between 1 and 100.')
        where=[]; params=[]
        for key in ('country','industry'):
            if filters.get(key): where.append(f'{key} LIKE %s'); params.append('%'+filters[key]+'%')
        clause=' WHERE '+' AND '.join(where) if where else ''
        conn=get_db_connection(); c=None
        try:
            c=conn.cursor(dictionary=True)
            c.execute('SELECT COUNT(*) AS total FROM businesses'+clause,tuple(params)); total=c.fetchone()['total']
            c.execute('SELECT * FROM businesses'+clause+' ORDER BY id DESC LIMIT %s OFFSET %s',tuple(params+[limit,(page-1)*limit]))
            return {'page':page,'limit':limit,'total_records':total,'total_pages':(total+limit-1)//limit,'data':c.fetchall()}
        finally:
            if c: c.close()
            conn.close()

    @staticmethod
    def update_business(business_id,data):
        BusinessService.validate_business_data(data,True)
        existing=BusinessService.get_business_by_id(business_id)
        if not existing: return None
        vals=[data.get(f,existing[f]) for f in FIELDS]
        vals=[v.strip() if isinstance(v,str) else v for v in vals]
        try:
            with db_transaction() as (_,c):
                c.execute('UPDATE businesses SET company_name=%s,registration_number=%s,country=%s,industry=%s,contact_email=%s,founded_year=%s WHERE id=%s',tuple(vals+[business_id]))
                c.execute('SELECT * FROM businesses WHERE id=%s',(business_id,))
                return c.fetchone()
        except mysql.connector.IntegrityError as e:
            if e.errno == mysql.connector.errorcode.ER_DUP_ENTRY: raise ValueError('A business with this registration number already exists.') from e
            raise

    @staticmethod
    def delete_business(business_id):
        with db_transaction() as (_,c):
            c.execute('DELETE FROM businesses WHERE id=%s',(business_id,))
            return c.rowcount>0
