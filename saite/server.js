const express = require('express');
const db = require('./db.js'); // Подключение к модулю базы данных
const path = require('path');
const app = express();
const port = 3000;

// Middleware для парсинга JSON
app.use(express.json());

// Маршрут для получения баллов пользователя по его ID
app.post('/update-points', (req, res) => {
  const userId = req.body.userId;
  const pointsToAdd = 100;

  // Сначала получаем текущие баллы пользователя
  db.getUserPointsById(userId, (err, currentPoints) => {
    if (err) {
      console.error('Ошибка при получении баллов пользователя:', err.message);
      res.status(500).json({ error: 'Internal Server Error' });
    } else {
      const newPoints = currentPoints + pointsToAdd;

      // Обновляем баллы пользователя
      db.updateUserPoints(userId, newPoints, (err) => {
        if (err) {
          console.error('Ошибка при обновлении баллов пользователя:', err.message);
          res.status(500).json({ error: 'Internal Server Error' });
        } else {
          console.log(`Баллы пользователя ${userId} успешно обновлены. Текущие баллы: ${newPoints}`);
          res.json({ success: true, points: newPoints });
        }
      });
    }
  });
});

// Маршрут для получения списка призов
app.get('/prizes', (req, res) => {
  console.log('Запрос на получение списка призов');
  db.getPrizes((err, prizes) => {
    if (err) {
      console.error('Ошибка при получении списка призов:', err.message);
      res.status(500).json({ error: 'Internal Server Error' });
    } else {
      console.log(`Список призов: ${JSON.stringify(prizes)}`);
      res.json({ prizes });
    }
  });
});

// Маршрут для обработки покупки приза
app.post('/buyPrize', (req, res) => {
  const { userId, prizeId } = req.body;
  console.log(`Запрос на покупку приза: userId=${userId}, prizeId=${prizeId}`);
  db.getUserPointsById(userId, (err, points) => {
    if (err) {
      console.error('Ошибка при получении баллов пользователя:', err.message);
      res.status(500).json({ error: 'Internal Server Error' });
    } else {
      console.log(`Баллы пользователя ${userId} перед покупкой: ${points}`);
      db.getPrizes((err, prizes) => {
        if (err) {
          console.error('Ошибка при получении списка призов:', err.message);
          res.status(500).json({ error: 'Internal Server Error' });
        } else {
          const prize = prizes.find(p => p.id === prizeId);
          if (prize && points >= prize.cost) {
            const newPoints = points - prize.cost;
            db.updateUserPoints(userId, newPoints, (err) => {
              if (err) {
                console.error('Ошибка при обновлении баллов пользователя:', err.message);
                res.status(500).json({ error: 'Internal Server Error' });
              } else {
                console.log(`Приз успешно куплен: userId=${userId}, prizeId=${prizeId}, newPoints=${newPoints}`);
                res.json({ message: 'Prize purchased successfully', newPoints });
              }
            });
          } else {
            console.log(`Недостаточно баллов или неверный приз: userId=${userId}, prizeId=${prizeId}, points=${points}`);
            res.status(400).json({ error: 'Insufficient points or invalid prize' });
          }
        }
      });
    }
  });
});

// Маршрут для получения баллов пользователя по его ID
app.get('/points/:userId', (req, res) => {
  const userId = req.params.userId;

  db.getUserPointsById(userId, (err, points) => {
    if (err) {
      console.error('Ошибка при получении баллов пользователя:', err.message);
      res.status(500).json({ error: 'Internal Server Error' });
    } else {
      res.json({ points });
    }
  });
});

// Обслуживание статических файлов
app.use(express.static(path.join(__dirname, 'public')));

// Запуск сервера
app.listen(port, (err) => {
  if (err) {
    console.error('Error starting server:', err);
  } else {
    console.log(`Server is running on http://localhost:${port}`);
  }
});
