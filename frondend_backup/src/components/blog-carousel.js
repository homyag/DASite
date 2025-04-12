// Класс для управления каруселью блога
class BlogCarousel {
  static selector() {
    return "[data-blog-section]";
  }

  constructor(node) {
    this.section = node;
    this.carousel = this.section.querySelector('#blog-carousel');
    this.slides = this.section.querySelectorAll('.blog-slide');
    this.prevButton = this.section.querySelector('#blog-prev');
    this.nextButton = this.section.querySelector('#blog-next');
    this.indicatorsContainer = this.section.querySelector('#blog-indicators');

    this.slidesPerView = 1;
    this.totalSlides = this.slides.length;
    this.currentSlide = 0;
    this.slideWidth = 0;
    this.autoplayInterval = null;

    this.init();
  }

  init() {
    // Подготавливаем бесконечную карусель
    this.prepareInfiniteCarousel();

    // Создаем индикаторы
    this.createIndicators();

    // Добавляем обработчики событий
    if (this.prevButton) {
      this.prevButton.addEventListener('click', () => this.prevSlide());
    }

    if (this.nextButton) {
      this.nextButton.addEventListener('click', () => this.nextSlide());
    }

    if (this.carousel) {
      this.carousel.addEventListener('transitionend', () => this.handleTransitionEnd());
    }

    // Обработчики для автопрокрутки
    const carouselContainer = this.carousel ? this.carousel.parentElement : null;
    if (carouselContainer) {
      carouselContainer.addEventListener('mouseenter', () => this.stopAutoplay());
      carouselContainer.addEventListener('mouseleave', () => this.startAutoplay());
    }

    // Обработка изменения размера окна
    window.addEventListener('resize', () => this.handleResize());

    // Запускаем автопрокрутку
    this.startAutoplay();
  }

  // Подготовка бесконечной карусели
  prepareInfiniteCarousel() {
    if (!this.carousel || !this.slides.length) return;

    // Определяем количество слайдов в зависимости от размера экрана
    this.updateSlidesPerView();

    // Удаляем предыдущие клоны, если они есть
    const existingClones = this.carousel.querySelectorAll('.clone');
    existingClones.forEach(clone => clone.remove());

    // Клонируем первые slidesPerView слайдов и добавляем их в конец
    for (let i = 0; i < this.slidesPerView; i++) {
      if (i < this.totalSlides) {
        const clone = this.slides[i].cloneNode(true);
        clone.classList.add('clone');
        this.carousel.appendChild(clone);
      }
    }

    // Клонируем последние slidesPerView слайдов и добавляем их в начало
    for (let i = this.totalSlides - 1; i >= Math.max(0, this.totalSlides - this.slidesPerView); i--) {
      const clone = this.slides[i].cloneNode(true);
      clone.classList.add('clone');
      this.carousel.insertBefore(clone, this.carousel.firstChild);
    }

    // Рассчитываем ширину слайда
    const carouselWidth = this.carousel.clientWidth;
    this.slideWidth = carouselWidth / this.slidesPerView;

    // Устанавливаем ширину для каждого слайда
    const allSlides = this.carousel.querySelectorAll('.blog-slide, .clone');
    allSlides.forEach(slide => {
      slide.style.minWidth = `${this.slideWidth}px`;
      slide.style.maxWidth = `${this.slideWidth}px`;
    });

    // Сдвигаем карусель влево для показа первого реального слайда
    this.carousel.style.transition = 'none';
    this.carousel.style.transform = `translateX(-${this.slideWidth * this.slidesPerView}px)`;

    // Форсируем перерисовку
    this.carousel.offsetHeight;
    this.carousel.style.transition = 'transform 500ms ease';
  }

  // Определяем количество слайдов в зависимости от размера экрана
  updateSlidesPerView() {
    const oldSlidesPerView = this.slidesPerView;

    this.slidesPerView = window.innerWidth < 768 ? 1 :
                       window.innerWidth < 1024 ? 2 : 3;

    return oldSlidesPerView !== this.slidesPerView;
  }

  // Создаем индикаторы
  createIndicators() {
    if (!this.indicatorsContainer) return;

    this.indicatorsContainer.innerHTML = '';
    for (let i = 0; i < this.totalSlides; i++) {
      const indicator = document.createElement('button');
      indicator.classList.add('w-3', 'h-3', 'rounded-full', 'mx-1', 'focus:outline-none');

      if (i === this.currentSlide) {
        indicator.classList.add('bg-indigo-600');
      } else {
        indicator.classList.add('bg-gray-300');
      }

      indicator.addEventListener('click', () => this.goToSlide(i));
      this.indicatorsContainer.appendChild(indicator);
    }
  }

  // Обновляем индикаторы
  updateIndicators() {
    if (!this.indicatorsContainer) return;

    const indicators = this.indicatorsContainer.querySelectorAll('button');
    indicators.forEach((indicator, index) => {
      if (index === this.currentSlide) {
        indicator.classList.add('bg-indigo-600');
        indicator.classList.remove('bg-gray-300');
      } else {
        indicator.classList.remove('bg-indigo-600');
        indicator.classList.add('bg-gray-300');
      }
    });
  }

  // Переход к определенному слайду
  goToSlide(index, animate = true) {
    this.currentSlide = index;

    // Проверяем границы
    if (this.currentSlide < 0) {
      this.currentSlide = this.totalSlides - 1;
    } else if (this.currentSlide >= this.totalSlides) {
      this.currentSlide = 0;
    }

    // Обновляем активный индикатор
    this.updateIndicators();

    // Смещение с учетом клонированных слайдов в начале
    const offset = -((this.currentSlide + this.slidesPerView) * this.slideWidth);

    if (this.carousel) {
      if (animate) {
        this.carousel.style.transition = 'transform 500ms ease';
      } else {
        this.carousel.style.transition = 'none';
      }

      this.carousel.style.transform = `translateX(${offset}px)`;
    }
  }

  // Переход к следующему слайду
  nextSlide() {
    this.goToSlide(this.currentSlide + 1);
  }

  // Переход к предыдущему слайду
  prevSlide() {
    this.goToSlide(this.currentSlide - 1);
  }

  // Обработка окончания перехода
  handleTransitionEnd() {
    // Если дошли до конца (показываем клон первого слайда)
    if (this.currentSlide >= this.totalSlides) {
      this.currentSlide = 0;
      this.carousel.style.transition = 'none';
      const offset = -((this.currentSlide + this.slidesPerView) * this.slideWidth);
      this.carousel.style.transform = `translateX(${offset}px)`;
      setTimeout(() => {
        this.carousel.style.transition = 'transform 500ms ease';
      }, 50);
    }

    // Если дошли до начала (показываем клон последнего слайда)
    if (this.currentSlide < 0) {
      this.currentSlide = this.totalSlides - 1;
      this.carousel.style.transition = 'none';
      const offset = -((this.currentSlide + this.slidesPerView) * this.slideWidth);
      this.carousel.style.transform = `translateX(${offset}px)`;
      setTimeout(() => {
        this.carousel.style.transition = 'transform 500ms ease';
      }, 50);
    }
  }

  // Обработка изменения размера окна
  handleResize() {
    const changed = this.updateSlidesPerView();

    if (changed) {
      // Перенастраиваем карусель
      this.prepareInfiniteCarousel();
      this.goToSlide(this.currentSlide, false);
    }
  }

  // Настройка автоматической прокрутки
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
}

export default BlogCarousel;