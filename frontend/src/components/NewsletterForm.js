/**
 * Компонент для обработки подписки на рассылку
 * с поддержкой уведомлений
 */
class NewsletterForm {
  constructor(formSelector = 'form.newsletter-form', options = {}) {
    // Настройки компонента по умолчанию
    this.options = {
      // Использовать ли AJAX отправку вместо стандартной
      useAjax: true,
      // Колбэки для различных событий
      onSuccess: null,
      onError: null,
      onSubmit: null,
      // Можно переопределить опции
      ...options
    };

    // Находим все формы подписки на странице
    this.forms = document.querySelectorAll(formSelector);

    if (this.forms.length) {
      this.init();
    }
  }

  init() {
    // Инициализируем каждую найденную форму
    this.forms.forEach(form => {
      // Если используем AJAX, перехватываем отправку формы
      if (this.options.useAjax) {
        form.addEventListener('submit', this.handleSubmit.bind(this));
      } else {
        // Иначе позволяем стандартную отправку, но добавляем базовую валидацию
        form.addEventListener('submit', this.validateForm.bind(this));
      }
    });
  }

  /**
   * Базовая валидация формы
   */
  validateForm(event) {
    const form = event.target;
    const emailField = form.querySelector('input[type="email"]');

    // Проверка заполнения поля email
    if (!emailField.value.trim()) {
      event.preventDefault();
      this.showFeedback(form, 'Пожалуйста, введите ваш email.', 'error');
      emailField.focus();

      if (this.options.onError) {
        this.options.onError('Пожалуйста, введите ваш email.');
      }

      return false;
    }

    // Базовая валидация email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(emailField.value.trim())) {
      event.preventDefault();
      this.showFeedback(form, 'Пожалуйста, введите корректный email адрес.', 'error');
      emailField.focus();

      if (this.options.onError) {
        this.options.onError('Пожалуйста, введите корректный email адрес.');
      }

      return false;
    }

    // Вызываем колбэк onSubmit, если он определен
    if (this.options.onSubmit) {
      this.options.onSubmit(form);
    }

    // Если всё в порядке, форма отправится стандартным способом
    return true;
  }

  /**
   * Получение CSRF токена из cookies
   */
  getCsrfToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Ищем cookie с названием 'csrftoken'
        if (cookie.substring(0, 10) === 'csrftoken=') {
          cookieValue = decodeURIComponent(cookie.substring(10));
          break;
        }
      }
    }
    return cookieValue;
  }

  /**
   * Обработчик отправки формы с использованием AJAX
   */
  handleSubmit(event) {
    event.preventDefault();

    // Если предварительная валидация не прошла
    if (!this.validateForm(event)) {
      return;
    }

    const form = event.target;
    const emailField = form.querySelector('input[type="email"]');
    const submitButton = form.querySelector('button[type="submit"]');
    const feedbackContainer = form.querySelector('.newsletter-feedback') || this.createFeedbackContainer(form);

    // Очищаем предыдущие сообщения
    feedbackContainer.innerHTML = '';
    feedbackContainer.classList.remove('text-red-500', 'text-green-500');

    // Вызываем колбэк onSubmit, если он определен
    if (this.options.onSubmit) {
      this.options.onSubmit(form);
    }

    // Изменяем состояние кнопки во время отправки
    const originalButtonText = submitButton.innerHTML;
    submitButton.disabled = true;
    submitButton.innerHTML = `
      <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      Отправка...
    `;

    // Получаем CSRF токен из формы или из cookies
    const csrfTokenElement = form.querySelector('input[name="csrfmiddlewaretoken"]');
    let csrfToken;

    if (csrfTokenElement) {
      csrfToken = csrfTokenElement.value;
    } else {
      csrfToken = this.getCsrfToken();
    }

    if (!csrfToken) {
      console.error('CSRF токен не найден. Используем стандартную отправку формы.');
      // Если нет CSRF токена, отправляем форму обычным способом
      form.submit();
      return;
    }

    // Отправляем AJAX запрос
    const formData = new FormData(form);

    fetch(form.action, {
      method: 'POST',
      body: formData,
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': csrfToken
      }
    })
    .then(response => {
      if (!response.ok) {
        if (response.status === 403) {
          throw new Error('Ошибка CSRF защиты. Используем стандартную отправку формы.');
        }
        throw new Error(`Ошибка сети: ${response.status} ${response.statusText}`);
      }
      return response.json();
    })
    .then(data => {
      // Возвращаем кнопку в исходное состояние
      submitButton.disabled = false;
      submitButton.innerHTML = originalButtonText;

      if (data.success) {
        // Очищаем форму при успехе
        form.reset();

        // Показываем сообщение в контейнере обратной связи
        this.showFeedback(form, data.message || 'Спасибо за подписку!', 'success');

        // Вызываем колбэк onSuccess, если он определен
        if (this.options.onSuccess) {
          this.options.onSuccess(data.message || 'Спасибо за подписку!');
        }
      } else {
        // Показываем сообщение об ошибке
        this.showFeedback(form, data.message || 'Произошла ошибка при подписке.', 'error');

        // Вызываем колбэк onError, если он определен
        if (this.options.onError) {
          this.options.onError(data.message || 'Произошла ошибка при подписке.');
        }
      }
    })
    .catch(error => {
      console.error('Ошибка:', error);

      // Если ошибка связана с CSRF, отправляем форму обычным способом
      if (error.message.includes('CSRF')) {
        form.submit();
        return;
      }

      // Возвращаем кнопку в исходное состояние
      submitButton.disabled = false;
      submitButton.innerHTML = originalButtonText;

      // Показываем сообщение об ошибке
      const errorMessage = 'Произошла ошибка при отправке. Пожалуйста, попробуйте позже.';
      this.showFeedback(form, errorMessage, 'error');

      // Вызываем колбэк onError, если он определен
      if (this.options.onError) {
        this.options.onError(errorMessage);
      }
    });
  }

  /**
   * Создаем контейнер для обратной связи, если его нет
   */
  createFeedbackContainer(form) {
    const container = document.createElement('div');
    container.className = 'newsletter-feedback mt-2 text-sm';
    form.appendChild(container);
    return container;
  }

  /**
   * Показываем сообщение обратной связи
   */
  showFeedback(form, message, type) {
    const feedbackContainer = form.querySelector('.newsletter-feedback') || this.createFeedbackContainer(form);
    feedbackContainer.textContent = message;

    if (type === 'error') {
      feedbackContainer.classList.add('text-red-500');
      feedbackContainer.classList.remove('text-green-500');
    } else {
      feedbackContainer.classList.add('text-green-500');
      feedbackContainer.classList.remove('text-red-500');
    }

    // Автоматически скрываем сообщение об успехе через 5 секунд
    if (type === 'success') {
      setTimeout(() => {
        feedbackContainer.textContent = '';
        feedbackContainer.classList.remove('text-green-500');
      }, 5000);
    }
  }
}

export default NewsletterForm;