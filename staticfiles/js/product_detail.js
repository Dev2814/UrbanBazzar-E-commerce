document.addEventListener("DOMContentLoaded", function () {
    // ===== Thumbnail Slider Logic =====
    const track = document.getElementById("thumbnailTrack");
    const leftBtn = document.querySelector(".thumb-scroll-btn.left");
    const rightBtn = document.querySelector(".thumb-scroll-btn.right");
  
    const thumbnailWidth = 80;
    const visibleCount = 3;
    const totalThumbnails = track.children.length;
    const maxOffset = (totalThumbnails - visibleCount) * thumbnailWidth;
    let currentOffset = 0;
  
    function updateSlider() {
      track.style.transform = `translateX(-${currentOffset}px)`;
    }
  
    rightBtn?.addEventListener("click", () => {
      if (currentOffset >= maxOffset) {
        currentOffset = 0;
      } else {
        currentOffset += visibleCount * thumbnailWidth;
        if (currentOffset > maxOffset) currentOffset = maxOffset;
      }
      updateSlider();
    });
  
    leftBtn?.addEventListener("click", () => {
      if (currentOffset <= 0) {
        currentOffset = maxOffset;
      } else {
        currentOffset -= visibleCount * thumbnailWidth;
        if (currentOffset < 0) currentOffset = 0;
      }
      updateSlider();
    });
  
    // ===== Related Products Scrollable Carousel Logic =====
    const relatedScrollTrack = document.getElementById("relatedScrollTrack");
    const relatedLeftBtn = document.getElementById("related-scroll-left");
    const relatedRightBtn = document.getElementById("related-scroll-right");
  
    let relatedOffset = 0;
    const relatedItemWidth = 250; // Adjust based on your card width + margin
    const visibleRelatedCount = 4;
    const totalRelatedItems = relatedScrollTrack?.children.length || 0;
    const relatedMaxOffset = (totalRelatedItems - visibleRelatedCount) * relatedItemWidth;
  
    function updateRelatedScroll() {
      relatedScrollTrack.style.transform = `translateX(-${relatedOffset}px)`;
    }
  
    relatedRightBtn?.addEventListener("click", () => {
      if (relatedOffset >= relatedMaxOffset) {
        relatedOffset = 0;
      } else {
        relatedOffset += visibleRelatedCount * relatedItemWidth;
        if (relatedOffset > relatedMaxOffset) relatedOffset = relatedMaxOffset;
      }
      updateRelatedScroll();
    });
  
    relatedLeftBtn?.addEventListener("click", () => {
      if (relatedOffset <= 0) {
        relatedOffset = relatedMaxOffset;
      } else {
        relatedOffset -= visibleRelatedCount * relatedItemWidth;
        if (relatedOffset < 0) relatedOffset = 0;
      }
      updateRelatedScroll();
    });
  
    // ===== Recommended Carousel Page-wise Logic (if needed) =====
    const recCarousel = document.getElementById("recommendedCarousel");
    const totalSlides = recCarousel?.children.length || 0;
    let recIndex = 0;
  
    window.scrollCarousel = function (direction) {
      recIndex += direction;
      if (recIndex < 0) recIndex = totalSlides - 1;
      if (recIndex >= totalSlides) recIndex = 0;
      recCarousel.style.transform = `translateX(-${recIndex * 100}%)`;
    };
  });
  
  // ===== Quantity Increment/Decrement =====
  function increase(event) {
    event.preventDefault();
    const input = document.getElementById("quantity");
    input.value = parseInt(input.value) + 1;
  }
  
  function decrease(event) {
    event.preventDefault();
    const input = document.getElementById("quantity");
    if (parseInt(input.value) > 1) {
      input.value = parseInt(input.value) - 1;
    }
  }
  