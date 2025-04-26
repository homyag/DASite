// Добавляем глобальное определение grecaptcha
/* global grecaptcha */
window.grecaptcha = window.grecaptcha || {};

// Функция валидации формы
function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');

    // Сбрасываем ошибки
    form.querySelectorAll('.error-message').forEach(el => el.remove());
    form.querySelectorAll('.border-red-500').forEach(el => el.classList.remove('border-red-500'));

    // Проверяем обязательные поля
    requiredFields.forEach(function(field) {
        if (!field.value.trim() && field.type !== 'checkbox') {
            isValid = false;
            field.classList.add('border-red-500');

            const errorMsg = document.createElement('p');
            errorMsg.classList.add('text-red-500', 'text-xs', 'mt-1', 'error-message');
            errorMsg.textContent = 'Это поле обязательно для заполнения';
            field.parentNode.insertBefore(errorMsg, field.nextSibling);
        } else if (field.type === 'checkbox' && !field.checked) {
            isValid = false;

            const checkboxContainer = field.closest('div');
            const errorMsg = document.createElement('p');
            errorMsg.classList.add('text-red-500', 'text-xs', 'mt-1', 'ml-8', 'error-message');
            errorMsg.textContent = 'Необходимо согласиться с условиями';
            checkboxContainer.appendChild(errorMsg);
        }
    });

    // Проверяем email
    const emailField = form.querySelector('input[type="email"]');
    if (emailField && emailField.value.trim()) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(emailField.value.trim())) {
            isValid = false;
            emailField.classList.add('border-red-500');

            const errorMsg = document.createElement('p');
            errorMsg.classList.add('text-red-500', 'text-xs', 'mt-1', 'error-message');
            errorMsg.textContent = 'Пожалуйста, введите корректный email';
            emailField.parentNode.insertBefore(errorMsg, emailField.nextSibling);
        }
    }

    // Проверяем телефон
    const phoneField = form.querySelector('input[type="tel"]');
    if (phoneField && phoneField.value.trim()) {
        // Получаем только цифры из телефона
        const digits = phoneField.value.replace(/\D/g, '');
        if (digits.length < 11) {
            isValid = false;
            phoneField.classList.add('border-red-500');

            const errorMsg = document.createElement('p');
            errorMsg.classList.add('text-red-500', 'text-xs', 'mt-1', 'error-message');
            errorMsg.textContent = 'Пожалуйста, введите полный номер телефона';
            phoneField.parentNode.insertBefore(errorMsg, phoneField.nextSibling);
        }
    }

    if (!isValid) {
        // Прокручиваем к первой ошибке
        const firstError = form.querySelector('.border-red-500, .error-message');
        if (firstError) {
            firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
            if (firstError.tagName !== 'P') {
                firstError.focus();
            }
        }
    }

    return isValid;
}

// Функция отображения ошибок валидации с сервера
function showFormValidationErrors(form, errors) {
    for (const fieldName in errors) {
        const field = form.querySelector(`[name="${fieldName}"]`);
        if (field) {
            field.classList.add('border-red-500');

            const errorMsg = document.createElement('p');
            errorMsg.classList.add('text-red-500', 'text-xs', 'mt-1', 'error-message');
            errorMsg.textContent = errors[fieldName].join(', ');
            field.parentNode.insertBefore(errorMsg, field.nextSibling);

            // Фокус на первое поле с ошибкой
            if (field === form.querySelector('.border-red-500')) {
                field.scrollIntoView({ behavior: 'smooth', block: 'center' });
                field.focus();
            }
        }
    }
}

// Применение маски для телефона
function applyPhoneMask(input) {
    input.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        let formattedValue = '';

        if (value.length > 0) {
            formattedValue = '+';
            if (value.length > 0) {
                formattedValue += value.substring(0, 1);
            }
            if (value.length > 1) {
                formattedValue += ' (' + value.substring(1, 4);
            }
            if (value.length > 4) {
                formattedValue += ') ' + value.substring(4, 7);
            }
            if (value.length > 7) {
                formattedValue += '-' + value.substring(7, 9);
            }
            if (value.length > 9) {
                formattedValue += '-' + value.substring(9, 11);
            }
        }

        e.target.value = formattedValue;
    });
}

// Добавление honeypot-поля
function addHoneypotField(form) {
    // Проверяем, есть ли уже honeypot-поле
    if (form.querySelector('input[name="website"]')) {
        return; // Поле уже существует, не добавляем дубликат
    }

    const honeypotField = document.createElement('div');
    honeypotField.className = 'hidden';
    honeypotField.innerHTML = `
        <input type="text" name="website" autocomplete="off" tabindex="-1" style="opacity: 0; position: absolute; z-index: -1;">
    `;
    form.appendChild(honeypotField);
}

// Получение CSRF токена из cookies
function getCsrfToken() {
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

// Основная функция инициализации формы
export function initContactForm() {
    // Находим все формы на странице
    const contactForms = document.querySelectorAll('#contact-form-element');

    contactForms.forEach(function(contactForm) {
        // Проверяем, что форма найдена
        if (!contactForm) {
            return;
        }

        // Создаем экземпляр попапа
        const popup = window.popup || null;
        const notification = window.notification || null;

        // Добавляем маску для телефона
        const phoneInput = contactForm.querySelector('input[type="tel"]');
        if (phoneInput) {
            applyPhoneMask(phoneInput);
        }

        // Добавляем honeypot-поле
        addHoneypotField(contactForm);

        // Обработчик отправки формы через AJAX
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();

            // Валидация формы
            if (!validateForm(contactForm)) {
                return false;
            }

            // Проверка honeypot-поля (если заполнено, это бот)
            const honeypotField = contactForm.querySelector('input[name="website"]');
            if (honeypotField && honeypotField.value) {
                if (notification) {
                    notification.show('Форма успешно отправлена!', 'success', 3000);
                } else if (popup && popup.showSuccessPopup) {
                    popup.showSuccessPopup();
                }
                return false;
            }

            // Показываем индикатор загрузки
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            if (!submitBtn) {
                return;
            }

            const originalBtnText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = `
                <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Отправка...
            `;

            // Собираем данные формы
            const formData = new FormData(contactForm);

            // Добавляем значение reCAPTCHA
            const recaptchaElement = contactForm.querySelector('.g-recaptcha');
            if (recaptchaElement) {
                const recaptchaResponse = grecaptcha.getResponse();
                if (!recaptchaResponse) {
                    const recaptchaError = document.createElement('p');
                    recaptchaError.classList.add('text-red-500', 'text-xs', 'mt-1', 'error-message');
                    recaptchaError.textContent = 'Пожалуйста, пройдите проверку reCAPTCHA';
                    recaptchaElement.parentNode.insertBefore(recaptchaError, recaptchaElement.nextSibling);
                    return false;
                }
                formData.append('g-recaptcha-response', recaptchaResponse);
            } else {
                return false;
            }

            // Добавляем информацию о странице
            formData.append('source_page', window.location.pathname);
            formData.append('source_url', window.location.href);

            // Добавляем трекинг для аналитики
            formData.append('form_submitted_at', new Date().toISOString());

            // Получаем CSRF токен
            const csrfToken = contactForm.querySelector('input[name="csrfmiddlewaretoken"]')
                ? contactForm.querySelector('input[name="csrfmiddlewaretoken"]').value
                : getCsrfToken();

            // Проверка наличия CSRF токена
            if (!csrfToken) {
                contactForm.submit();
                return;
            }

            // Выполняем AJAX запрос
            fetch(contactForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Ошибка сервера: ${response.status} ${response.statusText}`);
                }
                return response.json();
            })
            .then(data => {
                // Сбрасываем состояние кнопки
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;

                // Обрабатываем ответ
                if (data.errors) {
                    showFormValidationErrors(contactForm, data.errors);
                } else if (data.success) {
                    // Очищаем форму при успехе
                    contactForm.reset();

                    // Показываем уведомление об успехе
                    if (notification) {
                        notification.show(data.message || 'Заявка успешно отправлена!', 'success', 5000);
                    } else if (popup && popup.showSuccessPopup) {
                        popup.showSuccessPopup();
                    } else {
                        alert(data.message || 'Заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.');
                    }

                    // Задержка перед переадресацией, если указан URL
                    if (data.redirect_url) {
                        setTimeout(() => {
                            window.location.href = data.redirect_url;
                        }, 1500);
                    }
                }
            })
            .catch(() => {
                // Сбрасываем состояние кнопки
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;

                // Показываем сообщение об ошибке
                if (notification) {
                    notification.show('Произошла ошибка при отправке формы. Пожалуйста, попробуйте позже.', 'error', 5000);
                } else if (popup && popup.showErrorPopup) {
                    popup.showErrorPopup();
                } else {
                    alert('Произошла ошибка при отправке формы. Пожалуйста, попробуйте позже или свяжитесь с нами по телефону.');
                }
            });

            return false;
        });
    });
}

// Экспортируем функцию для обработки Django сообщений
export function handleDjangoMessages(messages) {
    if (!messages || messages.length === 0) return;

    if (window.notification) {
        messages.forEach(message => {
            window.notification.show(message.text, message.tags || 'info', 5000);
        });
    } else if (window.popup) {
        messages.forEach(message => {
            if (message.tags === 'error') {
                window.popup.showErrorPopup();
            } else if (message.tags === 'success') {
                window.popup.showSuccessPopup();
            }
        });
    }
}