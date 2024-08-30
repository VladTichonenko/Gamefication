// Установим локальные данные для тестирования
const userId = 1; // Замените на любое значение для тестирования

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
  document.body.classList.toggle('dark-theme');
  const themeIcon = document.getElementById('theme-icon');
  if (document.body.classList.contains('dark-theme')) {
    themeIcon.textContent = '🌜'; // Иконка луны для темной темы
  } else {
    themeIcon.textContent = '🌞'; // Иконка солнца для светлой темы
  }
}

// Отображение призов
(async () => {
  const prizes = await fetchPrizes();
  const points = await fetchUserPoints();
  updatePointsDisplay(points); // Обновляем отображение баллов при загрузке страницы

  const prizesContainer = document.getElementById('prizes');
  prizes.forEach(prize => {
    const prizeElement = document.createElement('div');
    prizeElement.classList.add('message');
    prizeElement.innerHTML = `
      <img src="${prize.image}" alt="${prize.name}" />
      <p>${prize.name}</p>
      <p>Cost: ${prize.cost} points</p>
      <button onclick="buyPrize(${prize.id})">Buy</button>
    `;
    prizesContainer.appendChild(prizeElement);
  });

  // Добавляем обработчик для кнопки переключения темы
  document.getElementById('theme-toggle').addEventListener('click', toggleTheme);
})();
