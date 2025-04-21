/* Price range */
$("#sl2").slider();
var RGBChange = function () {
  $("#RGB").css("background", "rgb(" + r.getValue() + "," + g.getValue() + "," + b.getValue() + ")");
};

/* Scroll to top */
$(document).ready(function () {
  $.scrollUp({
    scrollName: "scrollUp",
    scrollDistance: 300,
    scrollFrom: "top",
    scrollSpeed: 300,
    easingType: "linear",
    animation: "fade",
    animationSpeed: 200,
    scrollText: '<i class="fa fa-angle-up"></i>',
    zIndex: 2147483647,
  });
});

document.addEventListener("DOMContentLoaded", function () {
  // === Popup Auto Hide ===
  const popupContainer = document.getElementById("popupContainer");
  const popups = document.querySelectorAll(".popup");
  popups.forEach(popup => {
    setTimeout(() => {
      popup.classList.add("slide-up");
      setTimeout(() => popup.remove(), 500);
    }, 3000);
  });

  function showPopup(message, type = "success") {
    const popup = document.createElement("div");
    popup.className = `popup ${type}`;
    popup.innerHTML = message;
    popupContainer.appendChild(popup);
    setTimeout(() => {
      popup.classList.add("slide-up");
      setTimeout(() => popup.remove(), 500);
    }, 3000);
  }

  window.showPopup = showPopup;

  // === Recommended Products Slider ===
  const recommendedRow = document.querySelector(".slider-row");
  const recommendedSlides = document.querySelectorAll(".features-items .product-slide");
  const totalRecommended = recommendedSlides.length;
  const visibleRecommended = 9;
  let recommendedIndex = 0;

  function moveRecommendedSlider(step) {
    recommendedIndex += step;
    if (recommendedIndex < 0) recommendedIndex = totalRecommended - visibleRecommended;
    else if (recommendedIndex > totalRecommended - visibleRecommended) recommendedIndex = 0;
    recommendedRow.style.transform = `translateX(-${recommendedIndex * (100 / visibleRecommended)}%)`;
  }

  const recLeft = document.querySelector(".left-btn");
  const recRight = document.querySelector(".right-btn");

  if (recLeft && recRight && recommendedRow) {
    recLeft.addEventListener("click", () => moveRecommendedSlider(-1));
    recRight.addEventListener("click", () => moveRecommendedSlider(1));
  }

  // === Category Sliders ===
  document.querySelectorAll(".tab-pane").forEach((pane) => {
    const categoryId = pane.id.replace("category-", "");
    const sliderRow = pane.querySelector(`.category-slider-${categoryId}`);
    const slides = sliderRow ? sliderRow.querySelectorAll(".product-slide") : [];
    let catIndex = 0;
    const catVisible = 6;

    const leftCatBtn = pane.querySelector(".cat-left-btn");
    const rightCatBtn = pane.querySelector(".cat-right-btn");

    if (leftCatBtn && sliderRow) {
      leftCatBtn.addEventListener("click", () => {
        catIndex = (catIndex - 1 + slides.length) % slides.length;
        sliderRow.style.transform = `translateX(-${catIndex * (100 / catVisible)}%)`;
      });
    }

    if (rightCatBtn && sliderRow) {
      rightCatBtn.addEventListener("click", () => {
        catIndex = (catIndex + 1) % slides.length;
        sliderRow.style.transform = `translateX(-${catIndex * (100 / catVisible)}%)`;
      });
    }
  });

  // === Product Detail Image Slider ===
  const imageSlider = document.querySelector('.product-image-slider');
  const imgLeftBtn = document.querySelector('.product-img-left');
  const imgRightBtn = document.querySelector('.product-img-right');
  let currentImgIndex = 0;
  let autoplayInterval;

  if (imageSlider && imgLeftBtn && imgRightBtn) {
    const slides = imageSlider.querySelectorAll('.product-slide');

    const updateImageSlider = () => {
      const slideWidth = slides[0].offsetWidth;
      imageSlider.style.transform = `translateX(-${currentImgIndex * slideWidth}px)`;
    };

    const goToNextSlide = () => {
      currentImgIndex = (currentImgIndex + 1) % slides.length;
      updateImageSlider();
    };

    imgRightBtn.addEventListener('click', () => {
      currentImgIndex = (currentImgIndex + 1) % slides.length;
      updateImageSlider();
    });

    imgLeftBtn.addEventListener('click', () => {
      currentImgIndex = (currentImgIndex - 1 + slides.length) % slides.length;
      updateImageSlider();
    });

    window.addEventListener('resize', updateImageSlider);
    updateImageSlider(); // Initialize on load

    // === Autoplay every 4 seconds ===
    autoplayInterval = setInterval(goToNextSlide, 4000);
  }

  // === AJAX Add to Cart ===
  const forms = document.querySelectorAll('.add-to-cart-form');
  forms.forEach(form => {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      const url = form.getAttribute('data-url');
      const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;

      fetch(url, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(response => response.text())
      .then(message => {
        showPopup(message);
      })
      .catch(error => {
        console.error('Error adding to cart:', error);
      });
    });
  });
});
