import sqlite3 as sq

async def db_start():
    global db, cur
    db = sq.connect('priz.db')
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS items("
                "i_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "name TEXT, "
                "price TEXT, "
                "photo TEXT)")
    db.commit()

async def add_item(state):
    global db, cur
    async with state.proxy() as data:
        cur.execute("INSERT INTO items (name, price, photo) VALUES (?, ?, ?)",  # Исправлено на 'accounts'
                    (data['name'], data['price'], data['photo']))
        db.commit()


class DataBase:
    def __init__(self, db_file):
        self.connection = sq.connect(db_file)
        self.cursor = self.connection.cursor()
        self.create_tables()  # Создаем таблицы при инициализации

    def create_tables(self):
        self.cursor.execute('''
               CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER UNIQUE,
                   referer_id INTEGER
               )
           ''')
        self.connection.commit()  # Сохраняем изменения

    def user_exists(self, user_id):
        print("exists")
        with self.connection:
            result = self.connection.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, user_id, referer_id=None):
        with self.connection:
            print("adding user")
            if referer_id is not None:
                return self.cursor.execute("INSERT INTO users (user_id, referer_id) VALUES (?, ?)", (user_id, int(referer_id)))
            else:
                return self.cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))

    def count_referals(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT COUNT(id) as count FROM users WHERE referer_id = ?", (user_id,)).fetchone()[0]

    def __del__(self):
        self.connection.close()