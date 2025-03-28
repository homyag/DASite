class Testimonials {
  static selector() {
    return "[data-testimonials-slider]";
  }

  constructor(node) {
    this.node = node;
    this.slides = this.node.querySelectorAll('[data-testimonial]');
    this.prevButton = this.node.querySelector('[data-testimonial-prev]');
    this.nextButton = this.node.querySelector('[data-testimonial-next]');
    this.indicators = this.node.querySelectorAll('[data-testimonial-indicator]');
    this.currentIndex = 0;
    this.totalSlides = this.slides.length;
    this.autoplayInterval = null;

    this.init();
  }

  init() {
    // Hide all slides except the first one
    this.slides.forEach((slide, index) => {
      if (index !== 0) {
        slide.classList.add('hidden');
      }
    });

    // Set first indicator as active
    if (this.indicators.length > 0) {
      this.indicators[0].classList.add('bg-indigo-600');
      this.indicators[0].classList.remove('bg-gray-300');
    }

    // Add event listeners for buttons
    this.prevButton.addEventListener('click', () => {
      this.showPreviousSlide();
      this.resetAutoplay();
    });

    this.nextButton.addEventListener('click', () => {
      this.showNextSlide();
      this.resetAutoplay();
    });

    // Add click event for indicators
    this.indicators.forEach((indicator, index) => {
      indicator.addEventListener('click', () => {
        this.goToSlide(index);
        this.resetAutoplay();
      });
    });

    // Start autoplay
    this.startAutoplay();
  }

  startAutoplay() {
    this.autoplayInterval = setInterval(() => {
      this.showNextSlide();
    }, 5000); // Change slide every 5 seconds
  }

  resetAutoplay() {
    clearInterval(this.autoplayInterval);
    this.startAutoplay();
  }

  updateIndicators() {
    this.indicators.forEach((indicator, index) => {
      if (index === this.currentIndex) {
        indicator.classList.add('bg-indigo-600');
        indicator.classList.remove('bg-gray-300');
      } else {
        indicator.classList.remove('bg-indigo-600');
        indicator.classList.add('bg-gray-300');
      }
    });
  }

  goToSlide(index) {
    if (index === this.currentIndex) return;

    // Hide current slide
    this.slides[this.currentIndex].classList.add('hidden');

    // Update index
    this.currentIndex = index;

    // Show new slide
    this.slides[this.currentIndex].classList.remove('hidden');

    // Update indicators
    this.updateIndicators();
  }

  showPreviousSlide() {
    // Hide current slide
    this.slides[this.currentIndex].classList.add('hidden');

    // Update index
    this.currentIndex = (this.currentIndex - 1 + this.totalSlides) % this.totalSlides;

    // Show new slide
    this.slides[this.currentIndex].classList.remove('hidden');

    // Update indicators
    this.updateIndicators();
  }

  showNextSlide() {
    // Hide current slide
    this.slides[this.currentIndex].classList.add('hidden');

    // Update index
    this.currentIndex = (this.currentIndex + 1) % this.totalSlides;

    // Show new slide
    this.slides[this.currentIndex].classList.remove('hidden');

    // Update indicators
    this.updateIndicators();
  }
}

export default Testimonials;