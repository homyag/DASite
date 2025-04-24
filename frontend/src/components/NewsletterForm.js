/**
 * Компонент для обработки подписки на рассылку
 * с поддержкой уведомлений
 */
class NewsletterForm {
  constructor(formSelector, options) {
    // Инициализируем с дефолтными значениями
    formSelector = formSelector || 'form.newsletter-form';
    options = options || {};

    // Настройки компонента по умолчанию
    this.options = {
      // Использовать ли AJAX отправку вместо стандартной
      useAjax: true,
      // Колбэки для различных событий
      onSuccess: null,
      onError: null,
      onSubmit: null
    };

    // Копируем пользовательские опции
    for (var key in options) {
      if (Object.prototype.hasOwnProperty.call(options, key)) {
        this.options[key] = options[key];
      }
    }

    // Находим все формы подписки на странице
    this.forms = document.querySelectorAll(formSelector);

    if (this.forms.length) {
      this.init();
    }
  }

  init() {
    // Инициализируем каждую найденную форму
    var self = this;
    this.forms.forEach(function(form) {
      // Если используем AJAX, перехватываем отправку формы
      if (self.options.useAjax) {
        form.addEventListener('submit', self.handleSubmit.bind(self));
      } else {
        // Иначе позволяем стандартную отправку, но добавляем базовую валидацию
        form.addEventListener('submit', self.validateForm.bind(self));
      }
    });
  }

  /**
   * Базовая валидация формы
   */
  validateForm(event) {
    var form = event.target;

    // Проверяем существование поля email перед обращением к нему
    var emailField = form.querySelector('input[type="email"]');
    if (!emailField) {
      console.error('Ошибка: поле email не найдено в форме');
      event.preventDefault();

      // Создаем обратную связь для пользователя
      this.showFeedback(form, 'Ошибка в форме: отсутствует поле email.', 'error');

      if (this.options.onError) {
        this.options.onError('Ошибка в форме: отсутствует поле email.');
      }

      return false;
    }

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
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
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
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
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

    var form = event.target;
    var emailField = form.querySelector('input[type="email"]');

    // Защита от ошибки - проверяем наличие элементов перед использованием
    if (!emailField) {
      console.error('Email поле не найдено при отправке формы');
      return;
    }

    var submitButton = form.querySelector('button[type="submit"]');
    if (!submitButton) {
      console.error('Кнопка отправки не найдена в форме');
      return;
    }

    var feedbackContainer = form.querySelector('.newsletter-feedback') || this.createFeedbackContainer(form);

    // Очищаем предыдущие сообщения
    feedbackContainer.innerHTML = '';
    feedbackContainer.classList.remove('text-red-500', 'text-green-500');

    // Вызываем колбэк onSubmit, если он определен
    if (this.options.onSubmit) {
      this.options.onSubmit(form);
    }

    // Изменяем состояние кнопки во время отправки
    var originalButtonText = submitButton.innerHTML;
    submitButton.disabled = true;
    submitButton.innerHTML = '' +
      '<svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">' +
      '  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>' +
      '  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>' +
      '</svg>' +
      'Отправка...';

    // Получаем CSRF токен из формы или из cookies
    var csrfTokenElement = form.querySelector('input[name="csrfmiddlewaretoken"]');
    var csrfToken;

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
    var formData = new FormData(form);
    var self = this;

    fetch(form.action, {
      method: 'POST',
      body: formData,
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': csrfToken
      }
    })
    .then(function(response) {
      if (!response.ok) {
        if (response.status === 403) {
          throw new Error('Ошибка CSRF защиты. Используем стандартную отправку формы.');
        }
        throw new Error('Ошибка сети: ' + response.status + ' ' + response.statusText);
      }
      return response.json();
    })
    .then(function(data) {
      // Возвращаем кнопку в исходное состояние
      submitButton.disabled = false;
      submitButton.innerHTML = originalButtonText;

      if (data.success) {
        // Очищаем форму при успехе
        form.reset();

        // Проверяем, есть ли глобальный объект уведомлений
        if (window.notification && typeof window.notification.show === 'function') {
          // Используем глобальный компонент уведомлений для показа попапа
          window.notification.show(
            data.message || 'Спасибо за подписку!',
            'success',
            5000
          );
        } else if (window.popup && typeof window.popup.showSuccessPopup === 'function') {
          // Если есть глобальный попап компонент, используем его
          window.popup.showSuccessPopup();
        } else {
          // Резервный вариант - показываем уведомление в форме
          self.showFeedback(form, data.message || 'Спасибо за подписку!', 'success');
        }

        // Вызываем колбэк onSuccess, если он определен
        if (self.options.onSuccess) {
          self.options.onSuccess(data.message || 'Спасибо за подписку!');
        }
      } else {
        // Показываем сообщение об ошибке
        var errorMessage = data.message || 'Произошла ошибка при подписке.';

        // Проверяем, есть ли глобальный объект уведомлений
        if (window.notification && typeof window.notification.show === 'function') {
          // Используем глобальный компонент уведомлений для показа ошибки
          window.notification.show(errorMessage, 'error', 5000);
        } else if (window.popup && typeof window.popup.showErrorPopup === 'function') {
          // Если есть глобальный попап компонент, используем его
          window.popup.showErrorPopup();
        } else {
          // Резервный вариант - показываем уведомление в форме
          self.showFeedback(form, errorMessage, 'error');
        }

        // Вызываем колбэк onError, если он определен
        if (self.options.onError) {
          self.options.onError(errorMessage);
        }
      }
    })
    .catch(function(error) {
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
      var errorMessage = 'Произошла ошибка при отправке. Пожалуйста, попробуйте позже.';

      // Проверяем, есть ли глобальный объект уведомлений
      if (window.notification && typeof window.notification.show === 'function') {
        // Используем глобальный компонент уведомлений для показа ошибки
        window.notification.show(errorMessage, 'error', 5000);
      } else if (window.popup && typeof window.popup.showErrorPopup === 'function') {
        // Если есть глобальный попап компонент, используем его
        window.popup.showErrorPopup();
      } else {
        // Резервный вариант - показываем уведомление в форме
        self.showFeedback(form, errorMessage, 'error');
      }

      // Вызываем колбэк onError, если он определен
      if (self.options.onError) {
        self.options.onError(errorMessage);
      }
    });
  }

  /**
   * Создаем контейнер для обратной связи, если его нет
   */
  createFeedbackContainer(form) {
    var container = document.createElement('div');
    container.className = 'newsletter-feedback mt-2 text-sm';
    form.appendChild(container);
    return container;
  }

  /**
   * Показываем сообщение обратной связи
   */
  showFeedback(form, message, type) {
    var feedbackContainer = form.querySelector('.newsletter-feedback') || this.createFeedbackContainer(form);
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
      setTimeout(function() {
        feedbackContainer.textContent = '';
        feedbackContainer.classList.remove('text-green-500');
      }, 5000);
    }
  }
}

export default NewsletterForm;