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

window.document.addEventListener("DOMContentLoaded", function () {
  // Инициализация компонентов с выводом дополнительной информации
  try {
    // Инициализация Jumbotron
    const jumbotronElements = document.querySelectorAll(Jumbotron.selector());
    for (const elem of jumbotronElements) {
      new Jumbotron(elem);
    }
  } catch (error) {
    console.error("Ошибка при инициализации Jumbotron:", error);
  }
  
  try {
    // Инициализация карусели отзывов
    const testimonialsElements = document.querySelectorAll('[data-testimonials-carousel]');
    for (const elem of testimonialsElements) {
      new TestimonialsCarousel(elem);
    }
  } catch (error) {
    console.error("Ошибка при инициализации карусели отзывов:", error);
  }
  
  try {
    // Инициализация секции кейсов
    const casesElements = document.querySelectorAll('[data-cases-section]');
    for (const elem of casesElements) {
      new CasesCarousel(elem);
    }
  } catch (error) {
    console.error("Ошибка при инициализации секции кейсов:", error);
  }
  
  try {
    // Инициализация карусели блога
    const blogElements = document.querySelectorAll('[data-blog-section]');
    for (const elem of blogElements) {
      new BlogCarousel(elem);
    }
  } catch (error) {
    console.error("Ошибка при инициализации карусели блога:", error);
  }
  
  try {
    // Инициализация карусели партнеров
    const partnersElements = document.querySelectorAll('[data-partners-section]');
    for (const elem of partnersElements) {
      new PartnersCarousel(elem);
    }
  } catch (error) {
    console.error("Ошибка при инициализации карусели партнеров:", error);
  }

  try {
    // Инициализация формы контактов
    const contactForms = document.querySelectorAll('#contact-form-element');
    if (contactForms.length > 0) {
    // Импортируем и инициализируем класс ContactForm
    initContactForm();
  }
} catch (error) {
  console.error("Ошибка при инициализации контактной формы:", error);
}

try {
  // Инициализация компонента согласия на cookie
  new CookieConsent();
  console.log("Компонент согласия на cookie инициализирован");
} catch (error) {
  console.error("Ошибка при инициализации компонента согласия на cookie:", error);
}
});