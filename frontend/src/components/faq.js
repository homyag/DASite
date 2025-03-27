class FAQ {
  static selector() {
    return "[data-faq-accordion]";
  }

  constructor(node) {
    this.node = node;
    this.init();
  }

  init() {
    const buttons = this.node.querySelectorAll('[data-faq-button]');

    buttons.forEach((button) => {
      button.addEventListener('click', () => {
        const answer = button.nextElementSibling;
        const icon = button.querySelector('svg');

        // Check current state
        const isExpanded = button.getAttribute('aria-expanded') === 'true';

        // Toggle state
        if (isExpanded) {
          answer.classList.add('hidden');
          icon.classList.remove('rotate-180');
          button.setAttribute('aria-expanded', 'false');
        } else {
          answer.classList.remove('hidden');
          icon.classList.add('rotate-180');
          button.setAttribute('aria-expanded', 'true');
        }
      });
    });
  }
}

export default FAQ;