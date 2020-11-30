import sqlite3
import pandas as pd


class DataParent:

    def create_tables(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        if len(cursor.fetchall()) == 0:
            cursor.execute('''CREATE TABLE ads 
            (id integer primary key, job_id integer, title text, shop text, original_price real, 
            sale_price real, percent_off real, reviews int, paid_ad int, page_num int, ad_num int)''')
            cursor.execute('''CREATE TABLE jobs 
            (id integer primary key, job_name text, search_criteria text, status text)''')
            conn.commit()
        cursor.close()
        conn.close()


class DataStorage(DataParent):

    def __init__(self, session_name, search_criteria):
        self.session_name = session_name
        self.search_criteria = search_criteria
        self.db_name = 'database.db'
        self.create_tables()
        self.insert_job()

    def clear_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ads")
        conn.commit()
        cursor.close()
        conn.close()

    def complete_job(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("UPDATE jobs SET status = 'Completed' WHERE id = ?", [self.job_id])
        conn.commit()
        cursor.close()
        conn.close()

    def insert_job(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO jobs VALUES (?,?,?,?)", [
            None,
            self.session_name,
            self.search_criteria,
            'In Progress'
        ])
        conn.commit()
        cursor.execute("SELECT last_insert_rowid()")
        self.job_id = cursor.fetchall()[0][0]
        cursor.close()
        conn.close()

    def insert_ad(self, packet):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        for d in packet:
            cursor.execute("INSERT INTO ads VALUES (?,?,?,?,?,?,?,?,?,?,?)", [
                None,
                self.job_id,
                d["title"],
                d["shop"],
                d["original_price"],
                d["sale_price"],
                d["percent_off"],
                d["reviews"],
                d["paid_ad"],
                d["page_num"],
                d["ad_num"]]
                )
        conn.commit()
        cursor.close()
        conn.close()


class DataQuery(DataParent):

    def __init__(self):
        self.db_name = 'database.db'
        self.create_tables()

    def get_df(self, session_name):
        cols = ['job_name', 'search_criteria', 'title', 'shop', 'original_price',
                'sale_price', 'percent_off', 'reviews', 'paid_ad', 'page_num', 'ad_num']
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT jobs.job_name, jobs.search_criteria, "
                       f"ads.title, ads.shop, ads.original_price, ads.sale_price, "
                       f"ads.percent_off, ads.reviews, ads.paid_ad, ads.page_num, ads.ad_num "
                       f"FROM ads LEFT JOIN jobs ON ads.job_id = jobs.id WHERE jobs.job_name = ?", [session_name])
        d = cursor.fetchall()
        d = [dict(zip(cols, x)) for x in d]
        df = pd.DataFrame(d)
        cursor.close()
        conn.close()
        return df

    def get_jobs(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT job_name, search_criteria FROM jobs")
        return cursor.fetchall()

    def get_average_price(self, session_name):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT AVG(ads.sale_price) FROM ads LEFT JOIN jobs ON ads.job_id = jobs.id WHERE ads.paid_ad = 0 AND jobs.job_name = '{session_name}'")
        return cursor.fetchall()[0][0]

    def get_ad_count(self, session_name):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM ads LEFT JOIN jobs ON ads.job_id = jobs.id WHERE ads.paid_ad = 0 AND jobs.job_name = '{session_name}'")
        return cursor.fetchall()[0][0]