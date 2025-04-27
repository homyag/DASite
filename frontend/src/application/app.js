// This is the style entry file
import "../styles/index.css";

// Импорт базовых компонентов
import Notification from "../components/Notification";
import CookieConsent from "../components/CookieConsent";

window.document.addEventListener("DOMContentLoaded", async function () {
  // Инициализация базовых компонентов
  try {
    // Инициализация компонента уведомлений
    const notification = new Notification();
    notification.init();
  } catch (error) {
    console.error('Ошибка при инициализации уведомлений:', error);
  }

  try {
    // Инициализация компонента согласия на cookie
    const cookieConsent = new CookieConsent();
    cookieConsent.init();
  } catch (error) {
    console.error('Ошибка при инициализации cookie-согласия:', error);
  }

  // Ленивая загрузка компонентов
  try {
    // Инициализация Jumbotron
    const jumbotronElements = document.querySelectorAll('[data-jumbotron]');
    if (jumbotronElements.length > 0) {
      const { default: Jumbotron } = await import('../components/jumbotron');
      for (const elem of jumbotronElements) {
        const jumbotron = new Jumbotron(elem);
        jumbotron.init();
      }
    }
  } catch (error) {
    console.error('Ошибка при инициализации Jumbotron:', error);
  }

  try {
    // Инициализация карусели отзывов
    const testimonialsElements = document.querySelectorAll('[data-testimonials-carousel]');
    if (testimonialsElements.length > 0) {
      const { default: TestimonialsCarousel } = await import('../components/testimonials-carousel');
      for (const elem of testimonialsElements) {
        const testimonialsCarousel = new TestimonialsCarousel(elem);
        testimonialsCarousel.init();
      }
    }
  } catch (error) {
    console.error('Ошибка при инициализации карусели отзывов:', error);
  }

  try {
    // Инициализация секции кейсов
    const casesElements = document.querySelectorAll('[data-cases-section]');
    if (casesElements.length > 0) {
      const { default: CasesCarousel } = await import('../components/cases-carousel');
      for (const elem of casesElements) {
        const casesSection = new CasesCarousel(elem);
        casesSection.init();
      }
    }
  } catch (error) {
    console.error('Ошибка при инициализации секции кейсов:', error);
  }

  try {
    // Инициализация карусели блога
    const blogElements = document.querySelectorAll('[data-blog-section]');
    if (blogElements.length > 0) {
      const { default: BlogCarousel } = await import('../components/blog-carousel');
      for (const elem of blogElements) {
        const blogCarousel = new BlogCarousel(elem);
        blogCarousel.init();
      }
    }
  } catch (error) {
    console.error('Ошибка при инициализации карусели блога:', error);
  }

  try {
    // Инициализация карусели партнеров
    const partnersElements = document.querySelectorAll('[data-partners-section]');
    if (partnersElements.length > 0) {
      const { default: PartnersCarousel } = await import('../components/partners-carousel');
      for (const elem of partnersElements) {
        const partnersCarousel = new PartnersCarousel(elem);
        partnersCarousel.init();
      }
    }
  } catch (error) {
    console.error('Ошибка при инициализации карусели партнеров:', error);
  }

  try {
    // Инициализация формы контактов
    const contactForms = document.querySelectorAll('#contact-form-element');
    if (contactForms.length > 0) {
      const { default: ContactForm } = await import('../components/ContactForm');
      const contactForm = new ContactForm();
    }
  } catch (error) {
    console.error('Ошибка при инициализации формы контактов:', error);
  }

  try {
    // Инициализация формы подписки
    const newsletterForms = document.querySelectorAll('#newsletter-form');
    if (newsletterForms.length > 0) {
      const { default: NewsletterForm } = await import('../components/NewsletterForm');
      const newsletterForm = new NewsletterForm();
      newsletterForm.init();
    }
  } catch (error) {
    console.error('Ошибка при инициализации формы подписки:', error);
  }

  try {
    // Инициализация попапов
    const popupElements = document.querySelectorAll('[data-popup]');
    if (popupElements.length > 0) {
      const { default: Popup } = await import('../components/Popup');
      for (const elem of popupElements) {
        const popup = new Popup(elem);
        popup.init();
      }
    }
  } catch (error) {
    console.error('Ошибка при инициализации попапов:', error);
  }
});