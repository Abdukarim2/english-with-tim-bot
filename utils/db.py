import sqlite3


def get_course_category():
    con = sqlite3.connect("./db.sqlite3")
    cur = con.cursor()
    data = cur.execute(f"""
                            SELECT name FROM course_category
                       """).fetchall()

    con.close()
    return data


def get_course(category: str):
    con = sqlite3.connect("./db.sqlite3")
    cur = con.cursor()
    data = cur.execute(f"""
                    SELECT * FROM course WHERE category = '{category}'
               """).fetchall()
    con.close()
    return data


def get_teacher(category: str):
    con = sqlite3.connect("./db.sqlite3")
    cur = con.cursor()
    data = cur.execute(f"""
                    SELECT * FROM teacher WHERE category = '{category}'
               """).fetchall()
    con.close()
    return data


def getall_teacher():
    con = sqlite3.connect("./db.sqlite3")
    cur = con.cursor()
    data = cur.execute(f"""
                        SELECT name FROM teacher
                   """).fetchall()
    con.close()
    return data


def get_hour():
    con = sqlite3.connect("./db.sqlite3")
    cur = con.cursor()
    data = cur.execute(f"""
                        SELECT * FROM hour 
                   """).fetchall()
    con.close()
    return data


def get_day():
    con = sqlite3.connect("./db.sqlite3")
    cur = con.cursor()
    data = cur.execute(f"""
                        SELECT * FROM day 
                   """).fetchall()
    con.close()
    return data


def create_student(data: dict):
    con = sqlite3.connect("./db.sqlite3")
    cur = con.cursor()
    value = tuple(data.values())
    keys = tuple(data.keys())
    status = None
    try:
        cur.execute(f"""
                INSERT INTO student{keys} VALUES{value}
            """)
        status = 201
        con.commit()
    except sqlite3.Error as e:
        print(e)
        status = 400
    con.close()
    return status


def init():
    con = sqlite3.connect("./db.sqlite3")
    cur = con.cursor()
    cur.execute("""
                 CREATE TABLE IF NOT EXISTS
                    'course_category' (
                        'id' integer primary key AUTOINCREMENT,
                        'name' varchar(100)
                    )
    """)
    cur.execute("""
                CREATE TABLE IF NOT EXISTS
                    'course' (
                        'id' integer primary key AUTOINCREMENT,
                        'name' varchar(100),
                        'about' text,
                        'category' varchar(100)
                    )
            """)
    cur.execute("""
                CREATE TABLE IF NOT EXISTS
                    'teacher' (
                        'id' integer primary key AUTOINCREMENT,
                        'name' varchar(100),
                        'about' text,
                        'category' varchar(100),
                        'date' varchar(100)
                    )
            """)
    cur.execute("""
                CREATE TABLE IF NOT EXISTS
                    'hour' (
                        'id' integer primary key AUTOINCREMENT,
                        'hour' varchar(100)
                    )
            """)
    cur.execute("""
                CREATE TABLE IF NOT EXISTS
                    'day' (
                        'id' integer primary key AUTOINCREMENT,
                        'day' varchar(100)
                    )
            """)
    cur.execute("""
                CREATE TABLE IF NOT EXISTS
                    'student' (
                        'id' integer primary key AUTOINCREMENT,
                        'name' varchar(100),
                        'surname' varchar(100),
                        'number1' varchar(100),
                        'number2' varchar(20),
                        'username' varchar(100),
                        'userid' varchar(30),
                        'category' varchar(30)
                    )
            """)
    con.close()
