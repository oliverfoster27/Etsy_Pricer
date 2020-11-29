import sqlite3
import pandas as pd


class DataParent:

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        if len(cursor.fetchall()) == 0:
            cursor.execute('''CREATE TABLE ads 
            (session_name text, search_criteria text, title text, shop text, original_price real, sale_price real, percent_off real, 
            reviews int, paid_ad int, page_num int, ad_num int)''')
        cursor.close()
        conn.close()


class DataStorage(DataParent):

    def __init__(self, session_name, search_criteria):
        self.session_name = session_name
        self.search_criteria = search_criteria
        self.db_name = 'database.db'
        self.create_table()

    def clear_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ads")
        conn.commit()
        cursor.close()
        conn.close()

    def insert(self, packet):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        for d in packet:
            cursor.execute("INSERT INTO ads VALUES (?,?,?,?,?,?,?,?,?,?,?)", [
                self.session_name,
                self.search_criteria,
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
        self.create_table()

    def get_df(self, session_name):
        cols = ['session_name', 'search_criteria', 'title', 'shop', 'original_price',
                'sale_price', 'percent_off', 'reviews', 'paid_ad', 'page_num', 'ad_num']
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ads WHERE session_name = ?", [session_name])
        d = cursor.fetchall()
        d = [dict(zip(cols, x)) for x in d]
        df = pd.DataFrame(d)
        cursor.close()
        conn.close()
        return df

    def get_sessions(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT session_name, search_criteria FROM ads")
        return cursor.fetchall()

    def get_average_price(self, session_name):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT AVG(sale_price) FROM ads WHERE paid_ad = 0 AND session_name = '{session_name}'")
        return cursor.fetchall()[0][0]