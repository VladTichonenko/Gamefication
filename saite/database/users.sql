-- Создание таблицы users
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  referal_id INTEGER NOT NULL,
  points INTEGER DEFAULT 0
);

-- Создание таблицы prizes
CREATE TABLE IF NOT EXISTS prizes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  description TEXT,
  cost INTEGER NOT NULL,
  image TEXT
);

-- Добавление начальных данных в таблицу users
INSERT INTO users (user_id, referal_id, points) VALUES (1, 1, 100);
INSERT INTO users (user_id, referal_id, points) VALUES (2, 2, 200);

-- Добавление начальных данных в таблицу prizes
INSERT INTO prizes (name, description, cost, image) VALUES ('Teddy Bear', 'A cute teddy bear.', 50, 'teddy_bear.png');
INSERT INTO prizes (name, description, cost, image) VALUES ('Gift Card', 'A $10 gift card.', 100, 'gift_card.png');
