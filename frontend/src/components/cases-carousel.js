// Класс для управления каруселью кейсов и фильтрацией
class CasesCarousel {
  static selector() {
    return "[data-cases-section]";
  }

  constructor(node) {
    this.section = node;

    // Более надежные селекторы
    this.filterButtons = this.section.querySelectorAll('#case-filter-buttons button');
    this.carouselContainer = this.section.querySelector('#cases-carousel-container');
    this.gridContainer = this.section.querySelector('#cases-grid-container');
    this.carousel = this.section.querySelector('#cases-carousel');
    this.grid = this.section.querySelector('#cases-grid');
    this.prevButton = this.section.querySelector('#prev-slide');
    this.nextButton = this.section.querySelector('#next-slide');
    this.carouselIndicators = this.section.querySelector('#carousel-indicators');

    // Если не найдены основные элементы, прекращаем инициализацию
    if (!this.carousel || !this.filterButtons.length) {
      return;
    }

    // Сохраняем оригинальные карточки
    this.originalCards = Array.from(this.section.querySelectorAll('.case-card'));

    // Переменные для управления каруселью
    this.currentSlide = 0;
    this.slideWidth = 0;
    this.totalSlides = 0;
    this.cardsPerView = 1;

    this.init();
  }

  init() {
    // Инициализация карусели по умолчанию (показываем "Все кейсы")
    this.filterCases('all');

    // Обработчики для кнопок карусели
    if (this.prevButton) {
      this.prevButton.addEventListener('click', () => {
        if (this.currentSlide > 0) {
          this.currentSlide--;
          this.updateCarousel();
        }
      });
    }

    if (this.nextButton) {
      this.nextButton.addEventListener('click', () => {
        const maxSlide = Math.max(0, this.totalSlides - this.cardsPerView);
        if (this.currentSlide < maxSlide) {
          this.currentSlide++;
          this.updateCarousel();
        }
      });
    }

    // Обработчики для кнопок фильтрации
    this.filterButtons.forEach(button => {
      button.addEventListener('click', () => {
        // Получаем значение фильтра
        const filterValue = button.getAttribute('data-filter');

        // Обновляем стили кнопок
        this.filterButtons.forEach(btn => {
          btn.classList.remove('bg-indigo-600', 'text-white');
          btn.classList.add('bg-white', 'text-indigo-600', 'hover:border-indigo-600');
        });
        button.classList.remove('bg-white', 'text-indigo-600', 'hover:border-indigo-600');
        button.classList.add('bg-indigo-600', 'text-white');

        // Фильтруем кейсы
        this.filterCases(filterValue);
      });
    });

    // Обработка клавиатурной навигации для доступности
    document.addEventListener('keydown', (e) => {
      if (this.carouselContainer.classList.contains('hidden')) return;

      if (e.key === 'ArrowLeft' && !this.prevButton.disabled) {
        this.prevButton.click();
      } else if (e.key === 'ArrowRight' && !this.nextButton.disabled) {
        this.nextButton.click();
      }
    });

    // Адаптивность при изменении размера окна
    window.addEventListener('resize', () => {
      if (!this.carouselContainer.classList.contains('hidden')) {
        this.initCarousel();
      }
    });
  }

  // Инициализация карусели
  initCarousel() {
    if (!this.carousel) {
      return;
    }

    const cards = this.carousel.querySelectorAll('.case-card');
    this.totalSlides = cards.length;

    // Определяем количество карточек в одном слайде в зависимости от размера экрана
    if (window.innerWidth >= 1024) {
      this.cardsPerView = 3; // На больших экранах
    } else if (window.innerWidth >= 768) {
      this.cardsPerView = 2; // На средних экранах
    } else {
      this.cardsPerView = 1; // На маленьких экранах
    }

    // Количество индикаторов = всего слайдов - слайдов на экране + 1
    const indicatorCount = Math.max(1, this.totalSlides - this.cardsPerView + 1);

    // Очищаем и создаем индикаторы
    if (this.carouselIndicators) {
      this.carouselIndicators.innerHTML = '';
      for (let i = 0; i < indicatorCount; i++) {
        const indicator = document.createElement('span');
        indicator.classList.add('w-2', 'h-2', 'rounded-full', 'bg-indigo-200', 'cursor-pointer');
        if (i === 0) {
          indicator.classList.replace('bg-indigo-200', 'bg-indigo-600');
        }
        indicator.addEventListener('click', () => this.goToSlide(i));
        this.carouselIndicators.appendChild(indicator);
      }
    }

    // Получаем ширину одной карточки с учетом отступа
    if (cards.length > 0) {
      const firstCard = cards[0];
      const style = window.getComputedStyle(firstCard);
      const marginRight = parseInt(style.marginRight) || 0;
      this.slideWidth = firstCard.offsetWidth + marginRight;

      // Обновляем состояние карусели
      this.updateCarousel();
    }
  }

  // Перемещаем карусель к определенному слайду
  goToSlide(slideIndex) {
    this.currentSlide = slideIndex;
    this.updateCarousel();
  }

  // Обновляем состояние карусели
  updateCarousel() {
    // Перемещаем карусель
    if (this.carousel) {
      const translateValue = -this.currentSlide * this.slideWidth;
      this.carousel.style.transform = `translateX(${translateValue}px)`;
    }

    // Обновляем индикаторы
    if (this.carouselIndicators) {
      const indicators = this.carouselIndicators.querySelectorAll('span');
      indicators.forEach((indicator, index) => {
        if (index === this.currentSlide) {
          indicator.classList.replace('bg-indigo-200', 'bg-indigo-600');
        } else {
          indicator.classList.replace('bg-indigo-600', 'bg-indigo-200');
        }
      });
    }

    // Управляем доступностью кнопок
    if (this.prevButton) {
      this.prevButton.disabled = this.currentSlide === 0;
      this.prevButton.style.opacity = this.currentSlide === 0 ? '0.5' : '1';
    }

    if (this.nextButton) {
      const maxSlide = Math.max(0, this.totalSlides - this.cardsPerView);
      this.nextButton.disabled = this.currentSlide >= maxSlide;
      this.nextButton.style.opacity = this.currentSlide >= maxSlide ? '0.5' : '1';
    }
  }

  // Фильтрация кейсов
  filterCases(filterValue) {
    this.currentSlide = 0; // Сбрасываем позицию карусели

    if (filterValue === 'all') {
      // Для "Все кейсы" показываем карусель
      if (this.carouselContainer) {
        this.carouselContainer.classList.remove('hidden');
      }
      if (this.gridContainer) {
        this.gridContainer.classList.add('hidden');
      }

      // Очищаем и заполняем карусель всеми карточками
      if (this.carousel) {
        this.carousel.innerHTML = '';
        this.originalCards.forEach(card => {
          try {
            const clone = card.cloneNode(true);
            this.carousel.appendChild(clone);
          } catch {
            console.error('Ошибка при загрузке кейсов');
            // Показываем сообщение об ошибке пользователю
            if (window.notification) {
              window.notification.show('Произошла ошибка при загрузке кейсов. Пожалуйста, попробуйте позже.', 'error', 5000);
            }
          }
        });

        // Инициализируем карусель
        this.initCarousel();
      }

    } else {
      // Для фильтров показываем сетку
      if (this.carouselContainer) {
        this.carouselContainer.classList.add('hidden');
      }
      if (this.gridContainer) {
        this.gridContainer.classList.remove('hidden');
      }

      // Очищаем и заполняем сетку отфильтрованными карточками
      if (this.grid) {
        this.grid.innerHTML = '';
        let foundItems = 0;

        this.originalCards.forEach(card => {
          const categories = card.getAttribute('data-categories')?.split(',') || [];
          if (categories.includes(filterValue)) {
            try {
              const clone = card.cloneNode(true);
              this.grid.appendChild(clone);
              foundItems++;
            } catch {
              console.error('Ошибка при загрузке кейсов');
              // Показываем сообщение об ошибке пользователю
              if (window.notification) {
                window.notification.show('Произошла ошибка при загрузке кейсов. Пожалуйста, попробуйте позже.', 'error', 5000);
              }
            }
          }
        });

        // Если не найдено элементов, показываем сообщение
        if (foundItems === 0) {
          this.showNoItemsMessage();
        }
      }
    }

    // Добавляем анимацию появления
    const container = filterValue === 'all' ? this.carousel : this.grid;
    if (container) {
      container.style.opacity = '0';
      container.style.transition = 'opacity 0.3s ease-in-out';
      setTimeout(() => {
        container.style.opacity = '1';
      }, 50);
    }
  }

  showNoItemsMessage() {
    const emptyMessage = document.createElement('div');
    emptyMessage.className = 'col-span-full text-center py-12';
    emptyMessage.innerHTML = `
<p class="text-gray-500 text-lg">Кейсы по данной категории не найдены</p>
<button class="mt-4 px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
        data-filter="all">Показать все кейсы</button>
`;
    this.grid.appendChild(emptyMessage);

    // Добавляем обработчик для кнопки "Показать все кейсы"
    const showAllButton = this.grid.querySelector('button[data-filter="all"]');
    if (showAllButton) {
      showAllButton.addEventListener('click', () => {
        // Находим кнопку "Все кейсы" и имитируем клик
        const allButton = this.section.querySelector('button[data-filter="all"]');
        if (!allButton) {
          return;
        }
        allButton.click();
      });
    }
  }
}

export default CasesCarousel;