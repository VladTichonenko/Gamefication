import sqlite3 as sq
'''
async def db_start():
    global db, cur
    db = sq.connect('Gamefication/database/users.db')
    cur = db.cursor()
'''

async def db_start():
    global db, cur
    db = sq.connect('priz.db')
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS items("
                "i_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "name TEXT, "
                "price TEXT, "
                "discription None, "
                "photo TEXT)")
    db.commit()


class DataBase:
    def __init__(self, db_file):
        self.connection = sq.connect(db_file)
        self.cursor = self.connection.cursor()
        self.create_tables()  # Создаем таблицы при инициализации

    def create_tables(self):
        with self.connection:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    referal_id INTEGER,
                    points INTEGER DEFAULT 0
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS prizes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    cost INTEGER NOT NULL,
                    image TEXT
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    price REAL NOT NULL,
                    description TEXT,
                    photo TEXT
                )
            """)

    def user_exists(self, user_id):
        print("exists")
        with self.connection:
            result = self.connection.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, user_id, referer_id=None):
        with self.connection:
            print("adding user")
            if referer_id is not None:
                return self.cursor.execute("INSERT INTO users (user_id, referal_id, points) VALUES (?, ?, ?)", (user_id, int(referer_id), 0))
            else:
                return self.cursor.execute("INSERT INTO users (user_id, points) VALUES (?, ?)", (user_id, 0))

    def count_referals(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT COUNT(id) as count FROM users WHERE referal_id = ?", (user_id,)).fetchone()[0]
    
    def get_user_score(self, user_id):
        with self.connection:
            self.cursor.execute('SELECT points FROM users WHERE user_id = ?', (user_id,))
            result = self.cursor.fetchone()
            return result[0] if result else 0

    def update_user_score(self, user_id, points):
        with self.connection:
            # Проверяем, существует ли запись с данным user_id
            self.cursor.execute('SELECT points FROM users WHERE user_id = ?', (user_id,))
            result = self.cursor.fetchone()
            
            if result:
                # Если запись существует, обновляем очки
                self.cursor.execute('UPDATE users SET points = points + ? WHERE user_id = ?', (points, user_id))
            else:
                # Если записи нет, вставляем новую
                self.cursor.execute('INSERT INTO users (user_id, referal_id, points) VALUES (?, NULL, ?)', (user_id, points))
            
            self.connection.commit()

    def get_random_user_id(self):
        with self.connection:
            result = self.cursor.execute("SELECT user_id FROM users ORDER BY RANDOM() LIMIT 1").fetchone()
            return result[0] 

    async def add_item(self, state):
        async with state.proxy() as data:
            self.cursor.execute("INSERT INTO prizes (name, description,cost , image) VALUES (?, ?, ?, ?)",
                                (data['name'],None , data['price'], data['photo']))
            self.connection.commit()
    
    def get_all_user_ids(self):
        with self.connection:
            result = self.cursor.execute("SELECT user_id FROM users").fetchall()
            return [row[0] for row in result]

    def __del__(self):
        if hasattr(self, 'connection'):
            with self.connection:
                self.connection.close()


