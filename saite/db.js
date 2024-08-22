const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('./sql.db', (err) => {
  if (err) {
    console.error('Error opening database:', err);
  } else {
    console.log('Connected to the SQLite database.');
  }
});

function getUserPointsById(userId, callback) {
  db.get('SELECT points FROM users WHERE id = ?', [userId], (err, row) => {
    if (err) {
      console.error('Error fetching user points:', err);
      callback(err, null);
    } else {
      callback(null, row ? row.points : 0);
    }
  });
}

function getPrizes(callback) {
  db.all('SELECT * FROM prizes', (err, rows) => {
    if (err) {
      console.error('Error fetching prizes:', err);
      callback(err, null);
    } else {
      callback(null, rows);
    }
  });
}

function updateUserPoints(userId, newPoints, callback) {
  db.run('UPDATE users SET points = ? WHERE id = ?', [newPoints, userId], (err) => {
    if (err) {
      console.error('Error updating user points:', err);
      callback(err);
    } else {
      callback(null);
    }
  });
}

module.exports = {
  getUserPointsById,
  getPrizes,
  updateUserPoints
};
