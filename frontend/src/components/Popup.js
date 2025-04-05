// Класс для управления попапами
export default class Popup {
    constructor() {
        // Инициализируем класс
        this.container = null;
        this.contentElement = null;
        this.isInitialized = false;

        // Привязываем контекст this к методам для корректной работы колбэков
        this.closePopup = this.closePopup.bind(this);
        this.handleEscKey = this.handleEscKey.bind(this);

        // Инициализируем попап при создании класса
        this.initialize();
    }

    /**
     * Инициализирует попап, создает контейнер и настраивает обработчики событий
     */
    initialize() {
        if (this.isInitialized) return;

        // Создаем контейнер попапа
        this.createContainer();

        // Устанавливаем обработчики событий
        document.addEventListener('keydown', this.handleEscKey);

        // Отмечаем, что попап инициализирован
        this.isInitialized = true;
    }

    /**
     * Создает и настраивает контейнер попапа
     */
    createContainer() {
        // Проверяем, существует ли уже контейнер
        if (document.getElementById('popup-container')) {
            this.container = document.getElementById('popup-container');
            this.contentElement = this.container.querySelector('#popup-content');
            return;
        }

        // Создаем контейнер
        this.container = document.createElement('div');
        this.container.id = 'popup-container';
        this.container.className = 'fixed inset-0 z-50 flex items-center justify-center hidden';
        this.container.innerHTML = `
            <div class="fixed inset-0 bg-black bg-opacity-50 transition-opacity" id="popup-overlay"></div>
            <div class="relative bg-white rounded-lg shadow-xl max-w-md w-full mx-4 transform transition-all">
                <div id="popup-content"></div>
            </div>
        `;

        // Добавляем контейнер на страницу
        document.body.appendChild(this.container);

        // Сохраняем ссылку на элемент содержимого
        this.contentElement = this.container.querySelector('#popup-content');

        // Добавляем обработчик клика на оверлей
        this.container.querySelector('#popup-overlay').addEventListener('click', this.closePopup);
    }

    /**
     * Показывает попап с ошибкой отправки формы
     */
    showErrorPopup() {
        if (!this.isInitialized) this.initialize();

        this.contentElement.innerHTML = `
            <div class="p-6">
                <div class="flex items-center justify-between pb-3 border-b border-gray-200">
                    <h3 class="text-lg font-semibold text-red-600">Ошибка отправки формы</h3>
                    <button type="button" class="close-popup text-gray-400 hover:text-gray-500">
                        <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
                <div class="mt-4">
                    <p class="text-gray-700 mb-4">Приносим извинения, но возникла ошибка при отправке вашей заявки.</p>
                    <p class="text-gray-700 mb-4">Пожалуйста, попробуйте отправить форму ещё раз или свяжитесь с нами другим удобным способом:</p>
                    <div class="space-y-2 text-sm">
                        <div class="flex items-center">
                            <svg class="w-4 h-4 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                            </svg>
                            <span>+7 (999) 999-99-99</span>
                        </div>
                        <div class="flex items-center">
                            <svg class="w-4 h-4 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                            </svg>
                            <span>info@boldrise.ru</span>
                        </div>
                    </div>
                </div>
                <div class="mt-6 flex justify-end">
                    <button type="button" class="close-popup inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                        Закрыть
                    </button>
                </div>
            </div>
        `;

        // Добавляем обработчики кнопок закрытия
        this.contentElement.querySelectorAll('.close-popup').forEach(button => {
            button.addEventListener('click', this.closePopup);
        });

        // Показываем попап
        this.show();
    }

    /**
     * Показывает попап с успешной отправкой формы
     */
    showSuccessPopup() {
        if (!this.isInitialized) this.initialize();

        this.contentElement.innerHTML = `
            <div class="p-6">
                <div class="flex items-center justify-between pb-3 border-b border-gray-200">
                    <h3 class="text-lg font-semibold text-green-600">Заявка успешно отправлена</h3>
                    <button type="button" class="close-popup text-gray-400 hover:text-gray-500">
                        <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
                <div class="mt-4">
                    <div class="flex justify-center mb-4">
                        <div class="w-16 h-16 rounded-full bg-green-100 flex items-center justify-center">
                            <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                        </div>
                    </div>
                    <p class="text-gray-700 text-center mb-4">Спасибо! Ваша заявка успешно отправлена.</p>
                    <p class="text-gray-700 text-center">Мы свяжемся с вами в ближайшее время.</p>
                </div>
                <div class="mt-6 flex justify-center">
                    <button type="button" class="close-popup inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                        Закрыть
                    </button>
                </div>
            </div>
        `;

        // Добавляем обработчики кнопок закрытия
        this.contentElement.querySelectorAll('.close-popup').forEach(button => {
            button.addEventListener('click', this.closePopup);
        });

        // Показываем попап
        this.show();
    }

    /**
     * Показывает кастомный попап с заданным содержимым
     * @param {string} content - HTML содержимое попапа
     */
    showCustomPopup(content) {
        if (!this.isInitialized) this.initialize();

        this.contentElement.innerHTML = content;

        // Добавляем обработчики кнопок закрытия
        this.contentElement.querySelectorAll('.close-popup').forEach(button => {
            button.addEventListener('click', this.closePopup);
        });

        // Показываем попап
        this.show();
    }

    /**
     * Показывает попап
     */
    show() {
        // Показываем контейнер
        this.container.classList.remove('hidden');

        // Блокируем прокрутку страницы
        document.body.style.overflow = 'hidden';
    }

    /**
     * Закрывает попап
     */
    closePopup() {
        if (this.container) {
            this.container.classList.add('hidden');

            // Разблокируем прокрутку страницы
            document.body.style.overflow = '';
        }
    }

    /**
     * Обработчик нажатия клавиши ESC
     * @param {KeyboardEvent} event - Событие нажатия клавиши
     */
    handleEscKey(event) {
        if (event.key === 'Escape') {
            this.closePopup();
        }
    }
}