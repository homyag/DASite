// Класс для управления бесконечной каруселью отзывов (исправленный)
class TestimonialsCarousel {
  static selector() {
    return "[data-testimonials-carousel]";
  }

  constructor(node) {
    this.section = node;
    this.carousel = this.section.querySelector('.testimonials-slider');

    // Получаем все div непосредственно внутри .testimonials-slider
    this.slides = this.carousel ? Array.from(this.carousel.querySelectorAll(':scope > div')) : [];

    // Сохраняем количество оригинальных слайдов до клонирования
    this.originalSlides = this.slides.length;

    this.prevButton = this.section.querySelector('.testimonial-prev');
    this.nextButton = this.section.querySelector('.testimonial-next');
    this.indicatorsContainer = this.section.querySelector('.testimonial-indicators');

    // Устанавливаем переменную для отслеживания количества видимых слайдов
    this.slidesPerView = 1;
    this.currentSlide = 0;
    this.slideWidth = 0;
    this.autoplayInterval = null;
    this.isAnimating = false;

  }

  init() {
    // Добавляем класс 'initialized' к контейнеру для отладки
    this.section.classList.add('testimonials-carousel-initialized');

    // Вначале определяем количество слайдов и их ширину
    this.updateSlidesPerView();
    this.updateSlideWidth();

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
    window.addEventListener('resize', () => {
      this.handleResize();
    });

    // Переходим сразу к первому слайду (с учетом клонов)
    this.goToSlide(1, false);

    // Запускаем автопрокрутку
    this.startAutoplay();

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

  }

  // Подготовка бесконечной карусели
  prepareInfiniteCarousel() {
    if (!this.carousel || this.slides.length < 2) {
      return;
    }

    try {
      // Удаляем предыдущие клоны, если они есть
      const existingClones = this.carousel.querySelectorAll('.clone');
      existingClones.forEach(clone => clone.remove());

      // Сохраняем оригинальные слайды (без клонов)
      const originalSlides = Array.from(this.slides);

      // Клонируем начальные слайды и добавляем в конец
      // Клонируем количество слайдов, равное slidesPerView
      for (let i = 0; i < this.slidesPerView; i++) {
        const clone = originalSlides[i].cloneNode(true);
        clone.classList.add('clone');
        this.carousel.appendChild(clone);
      }

      // Клонируем конечные слайды и добавляем в начало
      // Берем последние slidesPerView слайдов
      for (let i = originalSlides.length - 1; i >= Math.max(0, originalSlides.length - this.slidesPerView); i--) {
        const clone = originalSlides[i].cloneNode(true);
        clone.classList.add('clone');
        this.carousel.insertBefore(clone, this.carousel.firstChild);
      }

      // Обновляем список слайдов с учетом клонов
      this.slides = Array.from(this.carousel.querySelectorAll(':scope > div'));

      // Устанавливаем ширину для каждого слайда
      this.slides.forEach(slide => {
        slide.style.minWidth = `${this.slideWidth}px`;
        slide.style.maxWidth = `${this.slideWidth}px`;
      });

      // Сдвигаем карусель для показа первого реального слайда
      // Рассчитываем отступ с учетом количества добавленных клонов
      const offset = -this.slideWidth * this.slidesPerView;
      this.carousel.style.transition = 'none';
      this.carousel.style.transform = `translateX(${offset}px)`;

      // Форсируем перерисовку
      this.carousel.offsetHeight;
      this.carousel.style.transition = 'transform 500ms ease';

      // Начальная позиция
      this.currentSlide = this.slidesPerView; // Индекс первого оригинального слайда

    } catch (_error) {
      console.error('Ошибка при загрузке отзывов:', _error);
      // Показываем сообщение об ошибке пользователю
      if (window.notification) {
        window.notification.show('Произошла ошибка при загрузке отзывов. Пожалуйста, попробуйте позже.', 'error', 5000);
      }
    }
  }

  updateSlideWidth() {
    if (this.carousel && this.section) {
      // Получаем ширину контейнера
      const containerWidth = this.section.clientWidth;

      // Учитываем отступы контейнера
      const style = window.getComputedStyle(this.section);
      const paddingLeft = parseFloat(style.paddingLeft) || 0;
      const paddingRight = parseFloat(style.paddingRight) || 0;

      // Доступная ширина контейнера
      const availableWidth = containerWidth - paddingLeft - paddingRight;

      // Рассчитываем размер промежутка между слайдами
      const windowWidth = window.innerWidth;
      let slideGap = 16; // Стандартный gap-4 в Tailwind (16px)

      if (windowWidth < 768) { // Мобильные устройства
        slideGap = 0; // Убираем зазор между слайдами на мобильных
        this.slideWidth = availableWidth; // Полная ширина для мобильных
      } else {
        // Вычисляем ширину одного слайда с учетом промежутков
        const gapTotal = slideGap * (this.slidesPerView - 1);
        this.slideWidth = (availableWidth - gapTotal) / this.slidesPerView;
      }

    }
  }

  // Переход к определенному слайду
  goToSlide(index, animate = true) {
    if (this.isAnimating) return;

    this.currentSlide = index;

    // Рассчитываем смещение
    const offset = -this.currentSlide * this.slideWidth;

    if (this.carousel) {
      if (animate) {
        this.carousel.style.transition = 'transform 500ms ease';
        this.isAnimating = true;
      } else {
        this.carousel.style.transition = 'none';
      }

      this.carousel.style.transform = `translateX(${offset}px)`;
    }

    // Обновляем индикаторы
    this.updateIndicators();

  }

  // Переход к следующему слайду
  nextSlide() {
    if (this.isAnimating) return;
    this.goToSlide(this.currentSlide + 1);
    this.resetAutoPlay();
  }

  // Переход к предыдущему слайду
  prevSlide() {
    if (this.isAnimating) return;
    this.goToSlide(this.currentSlide - 1);
    this.resetAutoPlay();
  }

  // Обработка окончания перехода
  handleTransitionEnd() {
    this.isAnimating = false;

    // Последний клонированный слайд
    const lastVisibleSlide = this.slides.length - this.slidesPerView;

    // Если дошли до крайних слайдов, перепрыгиваем без анимации
    if (this.currentSlide >= lastVisibleSlide) {
      // Перескок к началу (с клонированных слайдов на оригинальные)
      this.currentSlide = this.slidesPerView;
      this.carousel.style.transition = 'none';
      const offset = -this.currentSlide * this.slideWidth;
      this.carousel.style.transform = `translateX(${offset}px)`;

      // Восстанавливаем анимацию через небольшую задержку
      setTimeout(() => {
        this.carousel.style.transition = 'transform 500ms ease';
      }, 50);

    } else if (this.currentSlide < this.slidesPerView) {
      // Перескок к концу (с клонированных слайдов на оригинальные)
      this.currentSlide = lastVisibleSlide - this.slidesPerView;
      this.carousel.style.transition = 'none';
      const offset = -this.currentSlide * this.slideWidth;
      this.carousel.style.transform = `translateX(${offset}px)`;

      // Восстанавливаем анимацию через небольшую задержку
      setTimeout(() => {
        this.carousel.style.transition = 'transform 500ms ease';
      }, 50);

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
    // Учитываем клонированные слайды в начале
    let realIndex = (this.currentSlide - this.slidesPerView) % this.originalSlides;

    // Корректируем отрицательный индекс
    if (realIndex < 0) {
      realIndex = this.originalSlides + realIndex;
    }

    return realIndex;
  }

  // Обработка изменения размера окна
  handleResize() {
    // Сохраняем текущую реальную позицию
    const realIndex = this.getRealIndex();

    // Обновляем параметры
    this.updateSlidesPerView();
    this.updateSlideWidth();

    // Перестраиваем карусель с новыми параметрами
    this.prepareInfiniteCarousel();

    // Возвращаемся к тому же слайду, с которого начали
    const newPosition = realIndex + this.slidesPerView;
    this.goToSlide(newPosition, false);
  }

  // Автоматическое прокручивание
  startAutoplay() {
    this.stopAutoplay();
    this.autoplayInterval = setInterval(() => this.nextSlide(), 5000);
  }

  stopAutoplay() {
    if (this.autoplayInterval) {
      clearInterval(this.autoplayInterval);
      this.autoplayInterval = null;
    }
  }

  resetAutoPlay() {
    this.stopAutoplay();
    this.startAutoplay();
  }
}

export default TestimonialsCarousel;