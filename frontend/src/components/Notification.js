/**
 * Простой компонент для отображения уведомлений на странице
 */
class Notification {
  constructor() {
    this.container = null;
    this.timeout = null;
    this.init();
  }

  init() {
    // Создаем контейнер для уведомлений, если его еще нет
    if (!document.getElementById('notification-container')) {
      this.container = document.createElement('div');
      this.container.id = 'notification-container';
      this.container.className = 'fixed top-5 right-5 z-50 flex flex-col items-end space-y-2';
      document.body.appendChild(this.container);
    } else {
      this.container = document.getElementById('notification-container');
    }

    // Ищем уведомления Django messages при загрузке страницы
    this.processDjangoMessages();
  }

  /**
   * Показать уведомление
   * @param {string} message - текст уведомления
   * @param {string} type - тип уведомления (success, error, warning, info)
   * @param {number} duration - длительность отображения в миллисекундах
   */
  show(message, type = 'success', duration = 5000) {
    // Создаем элемент уведомления
    const notification = document.createElement('div');

    // Базовые классы для всех уведомлений
    const baseClasses = 'rounded-lg shadow-lg py-4 px-6 transform transition-all duration-300 max-w-md flex items-center';

    // Дополнительные классы в зависимости от типа
    let typeClasses = '';
    let icon = '';

    switch (type) {
      case 'success':
        typeClasses = 'bg-green-500 text-white';
        icon = `<svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>`;
        break;
      case 'error':
        typeClasses = 'bg-red-500 text-white';
        icon = `<svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>`;
        break;
      case 'warning':
        typeClasses = 'bg-yellow-500 text-white';
        icon = `<svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                </svg>`;
        break;
      case 'info':
      default:
        typeClasses = 'bg-blue-500 text-white';
        icon = `<svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>`;
        break;
    }

    // Применяем классы
    notification.className = `${baseClasses} ${typeClasses} translate-x-full opacity-0`;

    // Устанавливаем содержимое
    notification.innerHTML = `
      ${icon}
      <span>${message}</span>
      <button class="ml-4 text-white hover:text-gray-200 focus:outline-none">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
        </svg>
      </button>
    `;

    // Добавляем в контейнер
    this.container.appendChild(notification);

    // Обработчик закрытия
    const closeButton = notification.querySelector('button');
    closeButton.addEventListener('click', () => this.close(notification));

    // Анимируем появление через небольшую задержку
    setTimeout(() => {
      notification.classList.remove('translate-x-full', 'opacity-0');
    }, 10);

    // Автоматическое закрытие
    if (duration !== 0) {
      setTimeout(() => {
        this.close(notification);
      }, duration);
    }

    return notification;
  }

  /**
   * Закрыть уведомление
   * @param {Element} notification - элемент уведомления для закрытия
   */
  close(notification) {
    // Анимируем исчезновение
    notification.classList.add('translate-x-full', 'opacity-0');

    // Удаляем элемент после завершения анимации
    setTimeout(() => {
      if (notification.parentNode) {
        notification.parentNode.removeChild(notification);
      }
    }, 300);
  }

  /**
   * Обрабатывает Django сообщения, если они есть на странице
   */
  processDjangoMessages() {
    const messages = document.querySelectorAll('.django-message');

    messages.forEach(message => {
      const text = message.textContent.trim();
      const type = message.dataset.type || 'info';

      if (text) {
        this.show(text, type);

        // Удаляем сообщение из DOM, чтобы не показывать дважды
        message.parentNode.removeChild(message);
      }
    });
  }

  /**
   * Проверяет и обрабатывает сообщения в URL хэше
   * Например, #message=success:Подписка успешно оформлена
   */
  checkUrlMessages() {
    if (window.location.hash) {
      const hash = window.location.hash.substring(1);
      const params = new URLSearchParams(hash);

      if (params.has('message')) {
        const message = params.get('message');
        const [type, text] = message.split(':', 2);

        if (text) {
          this.show(text, type);

          // Очищаем хэш, чтобы сообщение не показывалось повторно при обновлении страницы
          history.replaceState(null, document.title, window.location.pathname + window.location.search);
        }
      }
    }
  }
}

export default Notification;