// This is the style entry file
import "../styles/index.css";

// Импорт компонентов
import Jumbotron from "../components/jumbotron";
import TestimonialsCarousel from "../components/testimonials-carousel";
import CasesCarousel from "../components/cases-carousel";
import BlogCarousel from "../components/blog-carousel";
import PartnersCarousel from "../components/partners-carousel";

window.document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM загружен, начинаем инициализацию компонентов");

  // Инициализация компонентов с выводом дополнительной информации
  try {
    // Инициализация Jumbotron
    const jumbotronElements = document.querySelectorAll(Jumbotron.selector());
    console.log(`Найдено элементов Jumbotron: ${jumbotronElements.length}`);
    for (const elem of jumbotronElements) {
      new Jumbotron(elem);
    }
  } catch (error) {
    console.error("Ошибка при инициализации Jumbotron:", error);
  }
  
  try {
    // Инициализация карусели отзывов
    const testimonialsElements = document.querySelectorAll('[data-testimonials-carousel]');
    console.log(`Найдено элементов карусели отзывов: ${testimonialsElements.length}`);
    for (const elem of testimonialsElements) {
      new TestimonialsCarousel(elem);
    }
  } catch (error) {
    console.error("Ошибка при инициализации карусели отзывов:", error);
  }
  
  try {
    // Инициализация секции кейсов
    const casesElements = document.querySelectorAll('[data-cases-section]');
    console.log(`Найдено элементов секции кейсов: ${casesElements.length}`);
    for (const elem of casesElements) {
      new CasesCarousel(elem);
    }
  } catch (error) {
    console.error("Ошибка при инициализации секции кейсов:", error);
  }
  
  try {
    // Инициализация карусели блога
    const blogElements = document.querySelectorAll('[data-blog-section]');
    console.log(`Найдено элементов карусели блога: ${blogElements.length}`);
    for (const elem of blogElements) {
      new BlogCarousel(elem);
    }
  } catch (error) {
    console.error("Ошибка при инициализации карусели блога:", error);
  }
  
  try {
    // Инициализация карусели партнеров
    const partnersElements = document.querySelectorAll('[data-partners-section]');
    console.log(`Найдено элементов карусели партнеров: ${partnersElements.length}`);
    for (const elem of partnersElements) {
      new PartnersCarousel(elem);
    }
  } catch (error) {
    console.error("Ошибка при инициализации карусели партнеров:", error);
  }
  
  console.log("Инициализация компонентов завершена");
});