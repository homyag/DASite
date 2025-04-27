// Добавляем глобальное определение grecaptcha
/* global grecaptcha */
window.grecaptcha = window.grecaptcha || {};

class ContactForm {
    constructor() {
        this.form = document.querySelector('#contact-form-element');
        this.notification = document.querySelector('.notification');
        this.submitButton = this.form?.querySelector('button[type="submit"]');
        this.originalButtonText = this.submitButton?.textContent;
        
        if (this.form) {
            console.log('Форма найдена:', this.form);
            this.init();
        } else {
            console.warn('Форма не найдена на странице');
        }
    }

    init() {
        this.form.addEventListener('submit', this.handleSubmit.bind(this));
        console.log('Обработчик submit добавлен');
        
        // Инициализация маски телефона
        const phoneInput = this.form.querySelector('input[type="tel"]');
        if (phoneInput) {
            this.applyPhoneMask(phoneInput);
            console.log('Маска телефона инициализирована');
        }

        // Добавляем honeypot-поле
        this.addHoneypotField(this.form);
        console.log('Honeypot-поле добавлено');
    }

    validateForm(form) {
        let isValid = true;
        const requiredFields = form.querySelectorAll('[required]');

        // Сбрасываем ошибки
        form.querySelectorAll('.error-message').forEach(el => el.remove());
        form.querySelectorAll('.border-red-500').forEach(el => el.classList.remove('border-red-500'));

        // Проверяем обязательные поля
        requiredFields.forEach(field => {
            if (!field.value.trim() && field.type !== 'checkbox') {
                isValid = false;
                field.classList.add('border-red-500');
                this.showFieldError(field, 'Это поле обязательно для заполнения');
            } else if (field.type === 'checkbox' && !field.checked) {
                isValid = false;
                const checkboxContainer = field.closest('div');
                this.showFieldError(checkboxContainer, 'Необходимо согласиться с условиями', true);
            }
        });

        // Проверяем email
        const emailField = form.querySelector('input[type="email"]');
        if (emailField?.value.trim()) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(emailField.value.trim())) {
                isValid = false;
                emailField.classList.add('border-red-500');
                this.showFieldError(emailField, 'Пожалуйста, введите корректный email');
            }
        }

        // Проверяем телефон
        const phoneField = form.querySelector('input[type="tel"]');
        if (phoneField?.value.trim()) {
            const digits = phoneField.value.replace(/\D/g, '');
            if (digits.length < 11) {
                isValid = false;
                phoneField.classList.add('border-red-500');
                this.showFieldError(phoneField, 'Пожалуйста, введите полный номер телефона');
            }
        }

        if (!isValid) {
            this.scrollToFirstError(form);
        }

        return isValid;
    }

    showFormValidationErrors(form, errors) {
        for (const fieldName in errors) {
            const field = form.querySelector(`[name="${fieldName}"]`);
            if (field) {
                field.classList.add('border-red-500');
                this.showFieldError(field, errors[fieldName].join(', '));
            }
        }
        this.scrollToFirstError(form);
    }

    applyPhoneMask(input) {
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

    addHoneypotField(form) {
        if (form.querySelector('input[name="website"]')) {
            return;
        }

        const honeypotField = document.createElement('div');
        honeypotField.className = 'hidden';
        honeypotField.innerHTML = `
            <input type="text" name="website" autocomplete="off" tabindex="-1" style="opacity: 0; position: absolute; z-index: -1;">
        `;
        form.appendChild(honeypotField);
    }

    getCsrfToken() {
        const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
        return csrfInput ? csrfInput.value : '';
    }

    showSuccessPopup(message = 'Спасибо! Ваше сообщение отправлено.') {
        if (document.getElementById('contact-success-popup')) return;

        const popup = document.createElement('div');
        popup.id = 'contact-success-popup';
        popup.className = 'fixed inset-0 flex items-center justify-center bg-black bg-opacity-40 z-50';
        
        popup.innerHTML = `
            <div class="bg-white rounded-xl max-w-[90vw] w-[400px] p-8 shadow-lg text-center relative">
                <button id="close-success-popup" class="absolute top-3 right-3 text-gray-500 text-2xl hover:text-gray-700">&times;</button>
                <svg class="mx-auto mb-4" width="48" height="48" fill="none" viewBox="0 0 24 24">
                    <circle cx="12" cy="12" r="12" fill="#e0f7e9"/>
                    <path d="M7 13l3 3 7-7" stroke="#34c759" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <div class="text-xl font-semibold text-gray-800 mb-2">Спасибо!</div>
                <div class="text-gray-600">${message}</div>
            </div>
        `;
        
        document.body.appendChild(popup);

        document.getElementById('close-success-popup').onclick = () => popup.remove();
        setTimeout(() => popup.remove(), 4000);
    }

    async handleSubmit(event) {
        // event.preventDefault(); // Убираем предотвращение стандартной отправки
        console.log('Начало отправки формы');
        
        if (!this.validateForm(this.form)) {
            event.preventDefault(); // Только если валидация не пройдена, отменяем отправку
            console.log('Валидация формы не пройдена');
            return;
        }
        // Если валидация прошла, форма отправится стандартно, а Django покажет алерт и сделает редирект
    }

    showFieldError(field, message, isCheckbox = false) {
        const errorMsg = document.createElement('p');
        errorMsg.className = 'text-red-500 text-xs mt-1 error-message';
        if (isCheckbox) {
            errorMsg.className += ' ml-8';
        }
        errorMsg.textContent = message;
        field.parentNode.insertBefore(errorMsg, field.nextSibling);
    }

    scrollToFirstError(form) {
        const firstError = form.querySelector('.border-red-500, .error-message');
        if (firstError) {
            firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
            if (firstError.tagName !== 'P') {
                firstError.focus();
            }
        }
    }

    showLoading() {
        if (this.submitButton) {
            this.submitButton.disabled = true;
            this.submitButton.classList.add('opacity-75', 'cursor-not-allowed');
            this.submitButton.innerHTML = `
                <svg class="animate-spin -ml-1 mr-2 h-5 w-5 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Отправка...
            `;
        }
    }

    hideLoading() {
        if (this.submitButton) {
            this.submitButton.disabled = false;
            this.submitButton.classList.remove('opacity-75', 'cursor-not-allowed');
            this.submitButton.textContent = this.originalButtonText;
        }
    }

    showNotification(message, type = 'success') {
        if (this.notification) {
            this.notification.textContent = message;
            this.notification.className = `notification ${type === 'success' ? 'success' : 'error'}`;
            this.notification.style.display = 'block';
            setTimeout(() => {
                this.notification.style.display = 'none';
            }, 5000);
        }
    }
}

export default ContactForm;