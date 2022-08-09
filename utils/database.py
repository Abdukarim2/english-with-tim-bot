import sys
import sqlite3
sys.path.append("..")
from configs.config import BASE_DIR


class Database:
    def __init__(self):
        self.db = BASE_DIR / 'db.sqlite3'

    def control(self, sql: str, commit: bool = False, fetchall: bool = False, fetchone: bool = False):
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        cur.execute(sql)
        data = []
        if commit:
            try:
                con.commit()
                return 200
            except sqlite3.IntegrityError:
                return 500
        else:
            if fetchone:
                data = cur.fetchone()
            if fetchall:
                data = cur.fetchall()
        con.close()
        return data

    def courses_teachers(self, table_name: str, category: str, name: str = None, about: str = None, all: bool = False):
        sql = ""
        if all == False:
            sql = f"""
                SELECT * FROM "{table_name}" WHERE category = "{category}" 
            """
        else:
            sql = f"""
                        SELECT * FROM "{table_name}" 
                 """
        result = self.control(sql, fetchall=True)
        if name is not None:
            sql = f"""
                    INSERT INTO "{table_name}"("name", "about", "category")
                    VALUES("{name}", "{about}", "{category}")
                """
            return self.control(sql, commit=True)
        return result

    def delete_db(self, table_name: str, where: str):
        sql = f"""
                DELETE FROM "{table_name}" WHERE name = "{where}"
                """
        return self.control(sql, commit=True)

    def users(self, name: str = None, surname: str = None,
              phone1: int = None, phone2: int = None,
              username: str = None, course: str = None, category: str = None):

        if name is not None:
            sql = f"""
                    INSERT INTO "users"("name", "surname", "phone1", "phone2", "username", "course")
                    VALUES("{name}", "{surname}", {phone1}, {phone2}, "{username}", "{course}")
                   """
            return self.control(sql, commit=True)
        elif category is not None:
            sql = f"""
                    SELECT * FROM  "users" WHERE course = "{category}"
                   """
            return self.control(sql, fetchall=True)

    def choose(self, table_name: str, where: str, delete: bool = False):

        if not delete:
            sql = f"""
                    SELECT * FROM "{table_name}" WHERE name = "{where}"
                    """
            return self.control(sql, fetchone=True)
        else:
            sql = f"""
                     DELETE FROM "{table_name}" WHERE name = "{where}"
                   """
            return self.control(sql, commit=True)


