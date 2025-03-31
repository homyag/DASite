// Класс для управления бесконечной каруселью отзывов (улучшенный)
class TestimonialsCarousel {
  static selector() {
    return "[data-testimonials-carousel]";
  }

  constructor(node) {
    this.section = node;
    this.carousel = this.section.querySelector('.testimonials-slider');

    // Получаем все div непосредственно внутри .testimonials-slider
    this.slides = this.carousel ? this.carousel.querySelectorAll(':scope > div') : [];

    console.log(`Найдено ${this.slides.length} слайдов в карусели отзывов`);

    this.prevButton = this.section.querySelector('.testimonial-prev');
    this.nextButton = this.section.querySelector('.testimonial-next');
    this.indicatorsContainer = this.section.querySelector('.testimonial-indicators');

    // Устанавливаем переменную для отслеживания количества видимых слайдов
    this.slidesPerView = 1;
    this.totalSlides = this.slides.length;
    this.currentSlide = 0;
    this.slideWidth = 0;
    this.autoplayInterval = null;
    this.isAnimating = false;

    console.log("Инициализация карусели отзывов:", {
      container: this.section,
      carousel: this.carousel,
      slides: this.slides.length,
      indicators: this.indicatorsContainer ? this.indicatorsContainer.children.length : 0,
      prevBtn: this.prevButton,
      nextBtn: this.nextButton
    });

    if (this.carousel && this.slides.length > 0) {
      this.init();
    } else {
      console.error("Не удалось найти необходимые элементы для карусели отзывов");
    }
  }

  init() {
    // Добавляем класс 'initialized' к контейнеру для отладки
    this.section.classList.add('testimonials-carousel-initialized');

    // Подготавливаем бесконечную карусель
    this.prepareInfiniteCarousel();

    // Добавляем обработчики событий
    if (this.prevButton) {
      this.prevButton.addEventListener('click', () => this.prevSlide());
    }

    if (this.nextButton) {
      this.nextButton.addEventListener('click', () => this.nextSlide());
    }

    // Обработчик окончания перехода для бесконечной прокрутки
    if (this.carousel) {
      this.carousel.addEventListener('transitionend', () => this.handleTransitionEnd());
    }

    // Обработчики для автопрокрутки
    if (this.carousel) {
      this.section.addEventListener('mouseenter', () => this.stopAutoplay());
      this.section.addEventListener('mouseleave', () => this.startAutoplay());
    }

    // Обработка изменения размера окна
    window.addEventListener('resize', () => this.handleResize());

    // Инициализация
    this.updateSlideWidth();

    // Переходим сразу к первому слайду
    this.goToSlide(0, false);

    // Запускаем автопрокрутку
    this.startAutoplay();

    console.log("Карусель отзывов инициализирована");
  }

  // Определение количества слайдов в зависимости от ширины экрана
  updateSlidesPerView() {
    const windowWidth = window.innerWidth;

    // Используем те же брейкпоинты, что и в Tailwind CSS
    if (windowWidth >= 1024) { // lg breakpoint
      this.slidesPerView = 3;
    } else if (windowWidth >= 768) { // md breakpoint
      this.slidesPerView = 2;
    } else {
      this.slidesPerView = 1;
    }

    console.log(`Обновлено количество отображаемых слайдов: ${this.slidesPerView}`);
  }

  // Подготовка бесконечной карусели
  prepareInfiniteCarousel() {
    if (!this.carousel || this.slides.length < 2) {
      console.warn("Недостаточно слайдов для бесконечной карусели");
      return;
    }

    try {
      // Удаляем предыдущие клоны, если они есть
      const existingClones = this.carousel.querySelectorAll('.clone');
      existingClones.forEach(clone => clone.remove());

      // Клонируем первый слайд и добавляем его в конец
      const firstSlideClone = this.slides[0].cloneNode(true);
      firstSlideClone.classList.add('clone');
      this.carousel.appendChild(firstSlideClone);

      // Клонируем последний слайд и добавляем его в начало
      const lastSlideClone = this.slides[this.totalSlides - 1].cloneNode(true);
      lastSlideClone.classList.add('clone');
      this.carousel.insertBefore(lastSlideClone, this.carousel.firstChild);

      // Обновляем список слайдов с учетом клонов
      this.slides = this.carousel.querySelectorAll(':scope > div');

      // Рассчитываем ширину слайда
      this.updateSlideWidth();

      // Устанавливаем ширину для каждого слайда
      this.slides.forEach(slide => {
        slide.style.minWidth = `${this.slideWidth}px`;
        slide.style.maxWidth = `${this.slideWidth}px`;
      });

      // Сдвигаем карусель влево для показа первого реального слайда
      this.carousel.style.transition = 'none';
      this.carousel.style.transform = `translateX(-${this.slideWidth}px)`;

      // Форсируем перерисовку
      this.carousel.offsetHeight;
      this.carousel.style.transition = 'transform 500ms ease';

      // Начальная позиция с учетом клона в начале
      this.currentSlide = 1; // Сейчас активен первый реальный слайд (после клона)

      console.log("Подготовлена бесконечная карусель отзывов, всего слайдов с клонами:", this.slides.length);
    } catch (error) {
      console.error("Ошибка при подготовке бесконечной карусели отзывов:", error);
    }
  }

  updateSlideWidth() {
  if (this.carousel && this.section) {
    // Обновляем количество видимых слайдов
    this.updateSlidesPerView();

    // Получаем ширину контейнера
    const containerWidth = this.section.clientWidth;

    // Учитываем отступы контейнера
    const style = window.getComputedStyle(this.section);
    const paddingLeft = parseFloat(style.paddingLeft) || 0;
    const paddingRight = parseFloat(style.paddingRight) || 0;

    // На мобильных устройствах удаляем отступы между слайдами
    const windowWidth = window.innerWidth;
    let slideGap = 0;

    if (windowWidth < 768) { // Мобильные устройства
      slideGap = 0; // Убираем зазор между слайдами на мобильных

      // Для мобильных устройств делаем слайд точно по размеру контейнера
      this.slideWidth = containerWidth - paddingLeft - paddingRight;
    } else {
      // Получаем размер промежутка (gap) между слайдами
      const carouselStyle = window.getComputedStyle(this.carousel);
      slideGap = parseInt(carouselStyle.gap) || 16; // значение gap-4 = 16px

      // Учитываем промежутки между слайдами при расчете ширины
      const totalGapWidth = slideGap * (this.slidesPerView - 1);

      // Вычисляем ширину одного слайда с учетом количества видимых слайдов и промежутков
      this.slideWidth = (containerWidth - paddingLeft - paddingRight - totalGapWidth) / this.slidesPerView;
    }

    console.log("Обновлена ширина слайда:", this.slideWidth, "Gap:", slideGap);
  }
}

  // Переход к определенному слайду
  goToSlide(index, animate = true) {
  if (this.isAnimating) return;

  this.currentSlide = index;

  // Проверяем границы
  if (this.currentSlide < 0) {
    this.currentSlide = this.totalSlides;
  } else if (this.currentSlide > this.totalSlides + 1) {
    this.currentSlide = 1;
  }

  // Обновляем активный индикатор
  this.updateIndicators();

  // Смещение с учетом клонированных слайдов
  let offset = -this.currentSlide * this.slideWidth;

  // На мобильных устройствах обеспечиваем точное позиционирование
  if (window.innerWidth < 768) {
    // Для мобильных - целое число пикселей
    offset = Math.round(offset);
  }

  if (this.carousel) {
    if (animate) {
      this.carousel.style.transition = 'transform 500ms ease';
      this.isAnimating = true;
    } else {
      this.carousel.style.transition = 'none';
    }

    this.carousel.style.transform = `translateX(${offset}px)`;
  }

  console.log("Переход к слайду:", this.currentSlide, "с отступом:", offset);
}

  // Переход к следующему слайду
  nextSlide() {
    if (this.isAnimating) return;
    this.goToSlide(this.currentSlide + 1);
    this.resetAutoPlay();
    console.log("Переход к следующему слайду");
  }

  // Переход к предыдущему слайду
  prevSlide() {
    if (this.isAnimating) return;
    this.goToSlide(this.currentSlide - 1);
    this.resetAutoPlay();
    console.log("Переход к предыдущему слайду");
  }

  // Обработка окончания перехода
  handleTransitionEnd() {
    this.isAnimating = false;

    // Если дошли до конца (показываем клон первого слайда)
    if (this.currentSlide > this.totalSlides) {
      this.currentSlide = 1;
      this.carousel.style.transition = 'none';
      const offset = -this.currentSlide * this.slideWidth;
      this.carousel.style.transform = `translateX(${offset}px)`;
      setTimeout(() => {
        this.carousel.style.transition = 'transform 500ms ease';
      }, 50);
      console.log("Переход в начало карусели");
    }

    // Если дошли до начала (показываем клон последнего слайда)
    if (this.currentSlide === 0) {
      this.currentSlide = this.totalSlides;
      this.carousel.style.transition = 'none';
      const offset = -this.currentSlide * this.slideWidth;
      this.carousel.style.transform = `translateX(${offset}px)`;
      setTimeout(() => {
        this.carousel.style.transition = 'transform 500ms ease';
      }, 50);
      console.log("Переход в конец карусели");
    }

    // Обновляем индикаторы
    this.updateIndicators();
  }

  // Обновляем индикаторы
  updateIndicators() {
    if (!this.indicatorsContainer) return;

    // Получаем реальный индекс (без учета клонов)
    const realIndex = this.getRealIndex();

    const indicators = this.indicatorsContainer.querySelectorAll('span');
    indicators.forEach((indicator, index) => {
      if (index === realIndex) {
        indicator.classList.remove('bg-indigo-200');
        indicator.classList.add('bg-indigo-600');
      } else {
        indicator.classList.remove('bg-indigo-600');
        indicator.classList.add('bg-indigo-200');
      }
    });
  }

  // Получаем индекс реального слайда (без учета клонов)
  getRealIndex() {
    if (this.currentSlide === 0) {
      return this.totalSlides - 1;
    } else if (this.currentSlide > this.totalSlides) {
      return 0;
    } else {
      return this.currentSlide - 1;
    }
  }

  // Обработка изменения размера окна
  handleResize() {
    // Обновляем ширину слайдов и количество видимых слайдов
    this.updateSlideWidth();

    // Применяем ширину к слайдам
    this.slides.forEach(slide => {
      slide.style.minWidth = `${this.slideWidth}px`;
      slide.style.maxWidth = `${this.slideWidth}px`;
    });

    // Обновляем позицию карусели
    const offset = -this.currentSlide * this.slideWidth;
    this.carousel.style.transition = 'none';
    this.carousel.style.transform = `translateX(${offset}px)`;

    // Форсируем перерисовку
    this.carousel.offsetHeight;
    this.carousel.style.transition = 'transform 500ms ease';
  }

  // Автоматическое прокручивание
  startAutoplay() {
    this.stopAutoplay();
    this.autoplayInterval = setInterval(() => this.nextSlide(), 5000);
    console.log("Запущено автопрокручивание карусели отзывов");
  }

  stopAutoplay() {
    if (this.autoplayInterval) {
      clearInterval(this.autoplayInterval);
      this.autoplayInterval = null;
      console.log("Остановлено автопрокручивание карусели отзывов");
    }
  }

  resetAutoPlay() {
    this.stopAutoplay();
    this.startAutoplay();
  }
}

export default TestimonialsCarousel;