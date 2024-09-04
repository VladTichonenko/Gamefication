const sqlite3 = require('sqlite3').verbose();
const path = require('path');

// Укажите правильный путь к базе данных
const dbPath = path.resolve(__dirname, 'database', 'E:/gemivication/Gamefication/saite/database/users.db');

const db = new sqlite3.Database(dbPath, (err) => {
  if (err) {
    console.error('Error opening database:', err.message);
  } else {
    console.log('Connected to the SQLite database.');
  }
});

function getUserPointsById(userId, callback) {
  const query = 'SELECT points FROM users WHERE id = ?';
  db.get(query, [userId], (err, row) => {
    if (err) {
      console.error('Error fetching user points:', err.message);
      callback(err, null);
    } else {
      if (row) {
        console.log(`User points for userId ${userId}: ${row.points}`);
        callback(null, row.points);
      } else {
        console.log(`No points found for userId ${userId}`);
        callback(null, 0);
      }
    }
  });
}

function getPrizes(callback) {
  const query = 'SELECT * FROM prizes';
  db.all(query, (err, rows) => {
    if (err) {
      console.error('Error fetching prizes:', err.message);
      callback(err, null);
    } else {
      console.log(`Prizes fetched: ${JSON.stringify(rows)}`);
      callback(null, rows);
    }
  });
}

function updateUserPoints(userId, newPoints, callback) {
  const query = 'UPDATE users SET points = ? WHERE id = ?';
  db.run(query, [newPoints, userId], (err) => {
    if (err) {
      console.error('Error updating user points:', err.message);
      callback(err);
    } else {
      console.log(`User points updated for userId ${userId}: ${newPoints}`);
      callback(null);
    }
  });
}

module.exports = {
  getUserPointsById,
  getPrizes,
  updateUserPoints
};
