// Класс для карусели партнеров
class PartnersCarousel {
  static selector() {
    return "[data-partners-section]";
  }

  constructor(node) {
    this.section = node;
    this.carousel = this.section.querySelector('.partners-carousel');

    // Пауза при наведении мыши
    if (this.carousel) {
      this.carousel.addEventListener('mouseenter', () => {
        this.carousel.style.animationPlayState = 'paused';
      });

      this.carousel.addEventListener('mouseleave', () => {
        this.carousel.style.animationPlayState = 'running';
      });
    }
  }
}

export default PartnersCarousel;