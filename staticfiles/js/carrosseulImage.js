const carousel = document.querySelector('.carousel');
const items = document.querySelectorAll('.carousel-item');
const prevButton = document.querySelector('.carousel-button.prev');
const nextButton = document.querySelector('.carousel-button.next');

let currentIndex = 0;

const updateCarousel = () => {
  const offset = -currentIndex * 100;
  carousel.style.transform = `translateX(${offset}%)`;

  items.forEach((item, index) => {
    item.classList.toggle('active', index === currentIndex);
  });
};

prevButton.addEventListener('click', () => {
  currentIndex = (currentIndex - 1 + items.length) % items.length;
  updateCarousel();
});

nextButton.addEventListener('click', () => {
  currentIndex = (currentIndex + 1) % items.length;
  updateCarousel();
});