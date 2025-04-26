// This is the style entry file
import "../styles/index.css";

// Импорт компонентов
import Jumbotron from "../components/jumbotron";
import TestimonialsCarousel from "../components/testimonials-carousel";
import CasesCarousel from "../components/cases-carousel";
import BlogCarousel from "../components/blog-carousel";
import PartnersCarousel from "../components/partners-carousel";
import { initContactForm } from "../components/ContactForm";
import CookieConsent from "../components/CookieConsent";
import NewsletterForm from "../components/NewsletterForm";
import Notification from "../components/Notification";
import Popup from "../components/Popup";

window.document.addEventListener("DOMContentLoaded", function () {
  // Инициализация компонентов с выводом дополнительной информации
  try {
    // Инициализация Jumbotron
    const jumbotronElements = document.querySelectorAll(Jumbotron.selector());
    for (const elem of jumbotronElements) {
      const jumbotron = new Jumbotron(elem);
      jumbotron.init();
    }
  } catch {
    return;
  }

  try {
    // Инициализация карусели отзывов
    const testimonialsElements = document.querySelectorAll('[data-testimonials-carousel]');
    for (const elem of testimonialsElements) {
      const testimonialsCarousel = new TestimonialsCarousel(elem);
      testimonialsCarousel.init();
    }
  } catch {
    return;
  }

  try {
    // Инициализация секции кейсов
    const casesElements = document.querySelectorAll('[data-cases-section]');
    for (const elem of casesElements) {
      const casesSection = new CasesCarousel(elem);
      casesSection.init();
    }
  } catch {
    return;
  }

  try {
    // Инициализация карусели блога
    const blogElements = document.querySelectorAll('[data-blog-section]');
    for (const elem of blogElements) {
      const blogCarousel = new BlogCarousel(elem);
      blogCarousel.init();
    }
  } catch {
    return;
  }

  try {
    // Инициализация карусели партнеров
    const partnersElements = document.querySelectorAll('[data-partners-section]');
    for (const elem of partnersElements) {
      const partnersCarousel = new PartnersCarousel(elem);
      partnersCarousel.init();
    }
  } catch {
    return;
  }

  try {
    // Инициализация формы контактов
    const contactForms = document.querySelectorAll('#contact-form-element');
    if (contactForms.length > 0) {
      // Импортируем и инициализируем класс ContactForm
      initContactForm();
    }
  } catch {
    return;
  }

  try {
    // Инициализация компонента согласия на cookie
    const cookieConsent = new CookieConsent();
    cookieConsent.init();
  } catch {
    return;
  }

  try {
    // Инициализация компонента уведомлений и сохранение его в глобальной области
    const notification = new Notification();
    notification.init();
  } catch {
    return;
  }

  try {
    // Инициализация компонента попапов (если он используется)
    const popup = new Popup();
    popup.init();
  } catch {
    // Если Popup не найден, это не критическая ошибка
    return;
  }

  try {
    // Инициализация форм подписки на рассылку
    // ВАЖНО: делаем это ПОСЛЕ инициализации notification и popup
    const newsletterForms = new NewsletterForm('.newsletter-form');
    newsletterForms.init();
  } catch {
    return;
  }
});