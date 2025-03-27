
// This is the style entry file
import "../styles/index.css";

// We can import other JS file as we like
import Jumbotron from "../components/jumbotron";
import FAQ from "../components/faq";
import Slider from "../components/slider";
import Testimonials from "../components/testimonials";

window.document.addEventListener("DOMContentLoaded", function () {
  window.console.log("dom ready");

  // Find elements and initialize
  for (const elem of document.querySelectorAll(Jumbotron.selector())) {
    new Jumbotron(elem);
  }
  // Initialize FAQ accordion
  for (const elem of document.querySelectorAll(FAQ.selector())) {
    new FAQ(elem);
  }

  // Initialize Services slider
  for (const elem of document.querySelectorAll(Slider.selector())) {
    new Slider(elem);
  }

  // Initialize Testimonials slider
  for (const elem of document.querySelectorAll(Testimonials.selector())) {
    new Testimonials(elem);
  }
});

