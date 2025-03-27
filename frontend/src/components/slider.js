class Slider {
  static selector() {
    return "[data-services-slider]";
  }

  constructor(node) {
    this.node = node;
    this.slides = this.node.querySelectorAll('[data-slide]');
    this.prevButton = this.node.querySelector('[data-slider-prev]');
    this.nextButton = this.node.querySelector('[data-slider-next]');
    this.currentIndex = 0;
    this.totalSlides = this.slides.length;

    this.init();
  }

  init() {
    // Hide all slides except the first one
    this.slides.forEach((slide, index) => {
      if (index !== 0) {
        slide.classList.add('hidden');
      }
    });

    // Add event listeners for buttons
    this.prevButton.addEventListener('click', () => this.showPreviousSlide());
    this.nextButton.addEventListener('click', () => this.showNextSlide());

    // Add keyboard navigation
    document.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') {
        this.showPreviousSlide();
      } else if (e.key === 'ArrowRight') {
        this.showNextSlide();
      }
    });
  }

  showPreviousSlide() {
    // Hide current slide
    this.slides[this.currentIndex].classList.add('hidden');

    // Update index
    this.currentIndex = (this.currentIndex - 1 + this.totalSlides) % this.totalSlides;

    // Show new slide
    this.slides[this.currentIndex].classList.remove('hidden');
  }

  showNextSlide() {
    // Hide current slide
    this.slides[this.currentIndex].classList.add('hidden');

    // Update index
    this.currentIndex = (this.currentIndex + 1) % this.totalSlides;

    // Show new slide
    this.slides[this.currentIndex].classList.remove('hidden');
  }
}

export default Slider;