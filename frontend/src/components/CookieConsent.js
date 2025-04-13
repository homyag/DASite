// frontend/src/components/CookieConsent.js
class CookieConsent {
  constructor() {
    this.consentKey = 'cookie_consent_accepted';
    this.container = null;
    this.modal = null;
    this.init();
  }

  init() {
    // Проверяем, было ли уже дано согласие
    if (this.hasUserConsent()) {
      return;
    }

    // Создаем плашку
    this.createConsentBanner();

    // Добавляем обработчики событий
    this.setupEventListeners();
  }

  // Проверка наличия согласия в localStorage
  hasUserConsent() {
    return localStorage.getItem(this.consentKey) === 'true';
  }

  // Создание HTML-элемента плашки
  createConsentBanner() {
    this.container = document.createElement('div');
    this.container.id = 'cookie-consent-banner';
    this.container.className = 'fixed bottom-0 left-0 right-0 bg-gray-900 text-white py-3 px-4 md:py-4 md:px-6 shadow-lg z-50 transform transition-transform duration-500';
    this.container.style.transform = 'translateY(100%)';

    this.container.innerHTML = `
      <div class="container mx-auto flex flex-col md:flex-row items-center justify-between">
        <div class="mb-3 md:mb-0 md:mr-8 text-sm md:text-base max-w-3xl">
          <p>
            Наш сайт использует файлы cookie для улучшения взаимодействия с вами. 
            Используя этот сайт, вы соглашаетесь с нашей 
            <a href="/privacy-policy/" class="text-indigo-400 hover:text-indigo-300 underline">политикой конфиденциальности</a> 
            и использованием cookie.
          </p>
        </div>
        <div class="flex flex-col sm:flex-row gap-2 shrink-0">
          <button id="accept-cookies" class="bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium py-1.5 px-3 md:py-2 md:px-4 rounded transition-colors">
            Принять все
          </button>
          <button id="cookie-settings" class="bg-transparent hover:bg-gray-700 text-white border border-white text-sm font-medium py-1.5 px-3 md:py-2 md:px-4 rounded transition-colors">
            Настройки
          </button>
        </div>
      </div>
    `;

    document.body.appendChild(this.container);

    // Анимация появления через небольшую задержку
    setTimeout(() => {
      this.container.style.transform = 'translateY(0)';
    }, 300);
  }

  // Создание модального окна настроек
  createSettingsModal() {
    // Проверяем, не создано ли уже модальное окно
    if (document.getElementById('cookie-settings-modal')) {
      return;
    }

    this.modal = document.createElement('div');
    this.modal.id = 'cookie-settings-modal';
    this.modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 opacity-0 transition-opacity duration-300';
    this.modal.style.visibility = 'hidden';

    // По умолчанию все галочки включены
    const savedSettings = this.getSavedCookieSettings();

    this.modal.innerHTML = `
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4 transform scale-95 transition-all duration-300">
        <div class="flex justify-between items-center border-b p-4">
          <h3 class="text-lg font-semibold text-gray-900">Настройки cookie</h3>
          <button id="close-settings-modal" class="text-gray-400 hover:text-gray-500">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div class="p-6">
          <p class="text-gray-600 mb-6">
            Вы можете выбрать, какие типы cookie мы можем использовать во время вашего пребывания на сайте.
            Нажмите на категории, чтобы переключить их состояние, и используйте кнопку «Сохранить настройки», чтобы подтвердить свой выбор.
          </p>
          
          <div class="space-y-4 mb-6">
            <div class="flex items-start">
              <div class="flex items-center h-5">
                <input id="cookie-necessary" name="cookie-necessary" type="checkbox" 
                  class="h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500" 
                  checked disabled>
              </div>
              <div class="ml-3">
                <label for="cookie-necessary" class="font-medium text-gray-700">Необходимые cookie</label>
                <p class="text-gray-500 text-sm">
                  Эти cookie необходимы для работы сайта. Без них сайт не сможет корректно функционировать. Эти cookie не могут быть отключены.
                </p>
              </div>
            </div>
            
            <div class="flex items-start">
              <div class="flex items-center h-5">
                <input id="cookie-analytics" name="cookie-analytics" type="checkbox" 
                  class="h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
                  ${savedSettings.analytics ? 'checked' : ''}>
              </div>
              <div class="ml-3">
                <label for="cookie-analytics" class="font-medium text-gray-700">Аналитические cookie</label>
                <p class="text-gray-500 text-sm">
                  Эти cookie позволяют собирать анонимную информацию о том, как пользователи взаимодействуют с нашим сайтом.
                  Это помогает нам улучшать функциональность и содержание сайта.
                </p>
              </div>
            </div>
            
            <div class="flex items-start">
              <div class="flex items-center h-5">
                <input id="cookie-functional" name="cookie-functional" type="checkbox" 
                  class="h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
                  ${savedSettings.functional ? 'checked' : ''}>
              </div>
              <div class="ml-3">
                <label for="cookie-functional" class="font-medium text-gray-700">Функциональные cookie</label>
                <p class="text-gray-500 text-sm">
                  Эти cookie помогают запоминать ваши предпочтения и персонализировать взаимодействие с сайтом.
                </p>
              </div>
            </div>
            
            <div class="flex items-start">
              <div class="flex items-center h-5">
                <input id="cookie-marketing" name="cookie-marketing" type="checkbox" 
                  class="h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
                  ${savedSettings.marketing ? 'checked' : ''}>
              </div>
              <div class="ml-3">
                <label for="cookie-marketing" class="font-medium text-gray-700">Маркетинговые cookie</label>
                <p class="text-gray-500 text-sm">
                  Эти cookie используются для показа релевантной рекламы и отслеживания маркетинговых кампаний.
                </p>
              </div>
            </div>
          </div>
          
          <div class="flex justify-end space-x-3">
            <button id="cancel-settings" 
              class="py-1.5 px-3 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
              Отмена
            </button>
            <button id="save-settings" 
              class="py-1.5 px-3 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
              Сохранить настройки
            </button>
          </div>
        </div>
      </div>
    `;

    document.body.appendChild(this.modal);

    // Добавляем обработчики событий для модального окна
    this.setupModalEventListeners();
  }

  // Получаем сохраненные настройки cookie или устанавливаем все по умолчанию
  getSavedCookieSettings() {
    const defaultSettings = {
      necessary: true,
      analytics: true,  // По умолчанию включено
      functional: true, // По умолчанию включено
      marketing: true   // По умолчанию включено
    };

    const savedSettings = localStorage.getItem('cookie_consent_settings');
    return savedSettings ? JSON.parse(savedSettings) : defaultSettings;
  }

  // Настройка обработчиков событий
  setupEventListeners() {
    if (!this.container) return;

    // Принять все cookie
    const acceptButton = this.container.querySelector('#accept-cookies');
    if (acceptButton) {
      acceptButton.addEventListener('click', () => {
        this.setConsent(true, 'all');
        this.hideBanner();
      });
    }

    // Открыть настройки cookie
    const settingsButton = this.container.querySelector('#cookie-settings');
    if (settingsButton) {
      settingsButton.addEventListener('click', () => {
        this.createSettingsModal();
        this.showModal();
      });
    }
  }

  // Настройка обработчиков событий для модального окна
  setupModalEventListeners() {
    if (!this.modal) return;

    // Закрыть модальное окно
    const closeButton = this.modal.querySelector('#close-settings-modal');
    if (closeButton) {
      closeButton.addEventListener('click', () => this.hideModal());
    }

    // Отмена настроек
    const cancelButton = this.modal.querySelector('#cancel-settings');
    if (cancelButton) {
      cancelButton.addEventListener('click', () => this.hideModal());
    }

    // Сохранение настроек
    const saveButton = this.modal.querySelector('#save-settings');
    if (saveButton) {
      saveButton.addEventListener('click', () => {
        this.saveSettings();
        this.hideModal();
        this.hideBanner();
      });
    }

    // Закрытие по клику вне модального окна
    this.modal.addEventListener('click', (e) => {
      if (e.target === this.modal) {
        this.hideModal();
      }
    });
  }

  // Показать модальное окно
  showModal() {
    if (!this.modal) return;

    this.modal.style.visibility = 'visible';

    // Форсируем перерисовку для плавной анимации
    this.modal.offsetHeight;

    this.modal.style.opacity = '1';
    this.modal.querySelector('div').classList.replace('scale-95', 'scale-100');

    // Блокируем прокрутку страницы
    document.body.style.overflow = 'hidden';
  }

  // Скрыть модальное окно
  hideModal() {
    if (!this.modal) return;

    this.modal.style.opacity = '0';
    this.modal.querySelector('div').classList.replace('scale-100', 'scale-95');

    // Разблокируем прокрутку страницы
    document.body.style.overflow = '';

    // Удаляем модальное окно после завершения анимации
    setTimeout(() => {
      this.modal.style.visibility = 'hidden';
    }, 300);
  }

  // Сохранение настроек пользователя
  saveSettings() {
    const settings = {
      necessary: true, // всегда включено
      analytics: this.modal.querySelector('#cookie-analytics').checked,
      functional: this.modal.querySelector('#cookie-functional').checked,
      marketing: this.modal.querySelector('#cookie-marketing').checked
    };

    localStorage.setItem('cookie_consent_settings', JSON.stringify(settings));
    localStorage.setItem(this.consentKey, 'true');

    // Установка уровня согласия
    if (settings.marketing) {
      localStorage.setItem('cookie_consent_level', 'all');
    } else if (settings.analytics || settings.functional) {
      localStorage.setItem('cookie_consent_level', 'partial');
    } else {
      localStorage.setItem('cookie_consent_level', 'necessary');
    }

    // Примените настройки (включите/выключите соответствующие скрипты)
    this.applySettings(settings);
  }

  // Применение настроек
  applySettings(settings) {
    // Ваш код для включения/отключения различных скриптов в зависимости от настроек

    // Пример: Если настройки аналитики отключены, удаляем Google Analytics
    if (!settings.analytics) {
      // Отключение Google Analytics и других аналитических скриптов
      this.disableAnalytics();
    }

    // Пример: Если маркетинговые cookie отключены, отключаем соответствующие скрипты
    if (!settings.marketing) {
      // Отключение маркетинговых скриптов
      this.disableMarketing();
    }

    console.log('Применены настройки cookie:', settings);
  }

  // Сохранение выбора пользователя
  setConsent(accepted, level = 'all') {
    localStorage.setItem(this.consentKey, accepted);
    localStorage.setItem('cookie_consent_level', level);

    // Создаем и сохраняем соответствующие настройки
    const settings = {
      necessary: true,
      analytics: level === 'all',
      functional: level === 'all',
      marketing: level === 'all'
    };

    localStorage.setItem('cookie_consent_settings', JSON.stringify(settings));

    // Применяем настройки
    this.applySettings(settings);
  }

  // Отключение аналитических скриптов
  disableAnalytics() {
    // Здесь код для отключения аналитических скриптов, например:
    // - Google Analytics
    // - Яндекс.Метрика
    // - и др.
    console.log('Аналитические cookie отключены');
  }

  // Отключение маркетинговых скриптов
  disableMarketing() {
    // Здесь код для отключения маркетинговых скриптов, например:
    // - Facebook Pixel
    // - Google Ads
    // - и др.
    console.log('Маркетинговые cookie отключены');
  }

  // Скрытие баннера
  hideBanner() {
    if (!this.container) return;

    this.container.style.transform = 'translateY(100%)';

    // Удаляем баннер после завершения анимации
    setTimeout(() => {
      if (this.container && this.container.parentNode) {
        this.container.parentNode.removeChild(this.container);
        this.container = null;
      }
    }, 500);
  }
}

export default CookieConsent;