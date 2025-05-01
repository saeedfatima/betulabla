const dropdown = document.querySelector('.dropdown');
let timeout;

dropdown.addEventListener('mouseenter', () => {
  clearTimeout(timeout);
  dropdown.classList.add('show');
  dropdown.querySelector('.dropdown-menu').classList.add('show');
});

dropdown.addEventListener('mouseleave', () => {
  timeout = setTimeout(() => {
    dropdown.classList.remove('show');
    dropdown.querySelector('.dropdown-menu').classList.remove('show');
  }, 200);
});