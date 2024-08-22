const express = require('express');
const db = require('./sql.db'); // Подключение к базе данных
const path = require('path');
const app = express();
const port = 3000;

// Middleware для парсинга JSON
app.use(express.json());

// Маршрут для получения баллов пользователя по его ID
app.get('/points/:userId', (req, res) => {
  const userId = req.params.userId;
  db.getUserPointsById(userId, (err, points) => {
    if (err) {
      res.status(500).json({ error: 'Internal Server Error' });
    } else {
      res.json({ points });
    }
  });
});

// Маршрут для получения списка призов
app.get('/prizes', (req, res) => {
  db.getPrizes((err, prizes) => {
    if (err) {
      res.status(500).json({ error: 'Internal Server Error' });
    } else {
      res.json({ prizes });
    }
  });
});

// Маршрут для обработки покупки приза
app.post('/buyPrize', (req, res) => {
  const { userId, prizeId } = req.body;
  db.getUserPointsById(userId, (err, points) => {
    if (err) {
      res.status(500).json({ error: 'Internal Server Error' });
    } else {
      db.getPrizes((err, prizes) => {
        if (err) {
          res.status(500).json({ error: 'Internal Server Error' });
        } else {
          const prize = prizes.find(p => p.id === prizeId);
          if (prize && points >= prize.cost) {
            const newPoints = points - prize.cost;
            db.updateUserPoints(userId, newPoints, (err) => {
              if (err) {
                res.status(500).json({ error: 'Internal Server Error' });
              } else {
                res.json({ message: 'Prize purchased successfully', newPoints });
              }
            });
          } else {
            res.status(400).json({ error: 'Insufficient points or invalid prize' });
          }
        }
      });
    }
  });
});

// Serve the HTML file
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Запуск сервера
app.listen(port, (err) => {
    if (err) {
      console.error('Error starting server:', err);
    } else {
      console.log(`Server is running on http://localhost:${port}`);
    }
  });
  