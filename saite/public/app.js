const userId = 1; // Получаем user_id из параметров запроса
console.log('Received user_id:', userId);
// Функция для получения баллов пользователя с сервера
async function fetchUserPoints() {
  try {
    const response = await fetch(`/points/${userId}`);
    const data = await response.json();
    console.log(`Баллы пользователя: ${data.points}`);
    return data.points;

  } catch (error) {
    console.error('Ошибка при получении баллов пользователя:', error);
    return 0;
  }
}

// Функция для получения списка призов с сервера
async function fetchPrizes() {
  try {
    const response = await fetch('/prizes');
    const data = await response.json();
    console.log(`Призы: ${JSON.stringify(data.prizes)}`);
    return data.prizes;
  } catch (error) {
    console.error('Ошибка при получении списка призов:', error);
    return [];
  }
}

// Функция для обновления отображения баллов на странице
function updatePointsDisplay(points) {
  document.getElementById('greeting').innerText = `Hello! You have ${points} points.`;
}

// Функция для покупки приза
async function buyPrize(prizeId) {
  try {
    const response = await fetch('/buyPrize', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ userId, prizeId })
    });
    const data = await response.json();
    if (data.error) {
      alert(data.error);
    } else {
      alert(`Приз успешно куплен! Новые баллы: ${data.newPoints}`);
      updatePointsDisplay(data.newPoints); // Обновляем отображение баллов
    }
  } catch (error) {
    console.error('Ошибка при покупке приза:', error);
  }
}

// Функция для переключения темы
function toggleTheme() {
  console.log('Тема переключается'); // Отладочное сообщение
  document.body.classList.toggle('dark-theme');
  const themeIcon = document.getElementById('theme-icon');
  if (document.body.classList.contains('dark-theme')) {
    themeIcon.textContent = '🌜'; // Иконка луны для темной темы
  } else {
    themeIcon.textContent = '🌞'; // Иконка солнца для светлой темы
  }
  // Сохраняем текущую тему в localStorage
  localStorage.setItem('theme', document.body.classList.contains('dark-theme') ? 'dark' : 'light');
}

// Устанавливаем тему при загрузке страницы
function setInitialTheme() {
  const savedTheme = localStorage.getItem('theme') || 'light';
  if (savedTheme === 'dark') {
    document.body.classList.add('dark-theme');
    document.getElementById('theme-icon').textContent = '🌜';
  }
}

// Отображение призов
(async () => {
  setInitialTheme(); // Устанавливаем тему при загрузке страницы
  const prizes = await fetchPrizes();
  const points = await fetchUserPoints();
  updatePointsDisplay(points); // Обновляем отображение баллов при загрузке страницы

  const prizesContainer = document.getElementById('prizes');
  prizes.forEach(prize => {
    const prizeElement = document.createElement('div');
    prizeElement.classList.add('message');
    prizeElement.innerHTML = `
      <img src="/GAmefication/img/${prize.image}" alt="${prize.name}" />
      <p>${prize.name}</p>
      <p>Cost: ${prize.cost} points</p>
      <button class="telegram-button"  onclick="buyPrize(${prize.id})">Buy</button>
    `;
    prizesContainer.appendChild(prizeElement);
  });

  // Добавляем обработчик для кнопки переключения темы
  document.getElementById('theme-toggle').addEventListener('click', toggleTheme);
})();


document.getElementById('navigate-button').addEventListener('click', () => {
  window.location.href = 'index1.html';
});

// app.js
document.addEventListener('DOMContentLoaded', () => {
  // Проверяем состояние кнопок при загрузке страницы
  ['channel1', 'channel2', 'channel3', 'channel4'].forEach(channelId => {
      if (localStorage.getItem(channelId) === 'subscribed') {
          document.getElementById(channelId).disabled = true;
      }
  });
});

async function subscribe(channelId, url) {
  // Открываем ссылку в новом окне
  window.open(url, '_blank');
  
  try {
      const response = await fetch('/update-points', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ userId, channelId })
      });
      const data = await response.json();
      if (data.error) {
          alert(data.error);
      } else {
          alert(`Вы успешно подписались на канал!`);
          // Делаем кнопку неактивной
          document.getElementById(channelId).disabled = true;
          // Сохраняем состояние в localStorage
          localStorage.setItem(channelId, 'subscribed');
      }
  } catch (error) {
      console.error('Ошибка при подписке:', error);
  }
}



