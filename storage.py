import sqlite3


class DataStorage:

    def __init__(self, session_name):
        self.session_name = session_name
        self.db_name = 'database.db'
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        if len(cursor.fetchall()) == 0:
            cursor.execute('''CREATE TABLE ads 
            (session_name text, title text, shop text, original_price real, sale_price real, percent_off real, 
            reviews int, paid_ad int, page_num int, ad_num int)''')
        cursor.close()
        conn.close()

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
            cursor.execute("INSERT INTO ads VALUES (?,?,?,?,?,?,?,?,?,?)", [
                self.session_name,
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
