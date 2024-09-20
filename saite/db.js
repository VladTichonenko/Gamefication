const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('E:/Gamefication/database/users.db'); // поменять путь на сервере 

// Функция для получения баллов пользователя по его ID
function getUserPointsById(userId, callback) {
  if (userId === undefined) {
    console.error('Error: userId is undefined');
    callback(new Error('userId is undefined'), null);
    return;
  }

  console.log(`Fetching points for userId: ${userId}`);
  const query = 'SELECT points FROM users WHERE id = ?';
  db.get(query, [userId], (err, row) => {
    if (err) {
      console.error('Error fetching user points:', err.message);
      callback(err, null);
    } else {
      console.log('Query result:', row);
      if (row && row.points !== undefined) {
        console.log(`User points for userId ${userId}: ${row.points}`);
        callback(null, row.points);
      } else {
        console.log(`No points found for userId ${userId}`);
        callback(null, 0);
      }
    }
  });
}

// Функция для обновления баллов пользователя
function updateUserPoints(userId, points, callback) {
  const query = 'UPDATE users SET points = ? WHERE id = ?';
  db.run(query, [points, userId], function(err) {
    if (err) {
      console.error('Error updating user points:', err.message);
      callback(err);
    } else {
      console.log(`Updated points for userId ${userId} to ${points}`);
      callback(null);
    }
  });
}

// Функция для получения списка призов
function getPrizes(callback) {
  const query = 'SELECT * FROM prizes';
  db.all(query, [], (err, rows) => {
    if (err) {
      console.error('Error fetching prizes:', err.message);
      callback(err, null);
    } else {
      console.log('Prizes fetched:', rows);
      callback(null, rows);
    }
  });
}

module.exports = {
  getUserPointsById,
  updateUserPoints,
  getPrizes
};
