function isElementFullyInViewport(el) {
  const rect = el.getBoundingClientRect();
  const windowHeight = window.innerHeight || document.documentElement.clientHeight;
  const windowWidth = window.innerWidth || document.documentElement.clientWidth;

  return rect.top >= 0 && rect.left >= 0 && rect.bottom <= windowHeight && rect.right <= windowWidth;
}

function isElementInViewport(el) {
  const rect = el.getBoundingClientRect();
  const windowHeight = window.innerHeight || document.documentElement.clientHeight;
  const windowWidth = window.innerWidth || document.documentElement.clientWidth;

  return rect.bottom >= 0 && rect.right >= 0 && rect.top <= windowHeight && rect.left <= windowWidth;
}

export { isElementInViewport, isElementFullyInViewport };
