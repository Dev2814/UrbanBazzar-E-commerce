// // Close modal function (last one will override earlier if same function name)
// function closeModal() {
//   document.getElementById("generated-modal").style.display = "none";
// }

// // Preview image using FileReader (from 1st JS)
// document
//   .getElementById("upload-input")
//   .addEventListener("change", function (e) {
//     const file = e.target.files[0];
//     const previewBox = document.getElementById("preview-box");
//     if (file) {
//       const reader = new FileReader();
//       reader.onload = function (event) {
//         previewBox.innerHTML = `<img src="${event.target.result}" alt="Preview Image">`;
//       };
//       reader.readAsDataURL(file);
//     }
//   });

// // Additional preview logic using URL.createObjectURL (from 2nd JS)
// const uploadInput = document.getElementById("upload-input");
// const previewBox = document.getElementById("preview-box");
// const generatedModal = document.getElementById("generated-modal");

// uploadInput.addEventListener("change", function (event) {
//   const file = event.target.files[0];
//   previewBox.innerHTML = "";

//   if (file && file.type.startsWith("image/")) {
//     const img = document.createElement("img");
//     img.src = URL.createObjectURL(file);
//     img.onload = () => URL.revokeObjectURL(img.src);
//     previewBox.appendChild(img);
//   } else {
//     previewBox.innerHTML = "<p>Please select a valid image file.</p>";
//   }
// });

// function showGeneratedImage() {
//   generatedModal.style.display = "flex";
// }

// // Overridden closeModal function (from 2nd JS)
// function closeModal() {
//   generatedModal.style.display = "none";
// }

// === Image Preview Functionality ===
document.addEventListener("DOMContentLoaded", function () {
    const uploadInput = document.getElementById("upload-input");
    const previewBox = document.getElementById("preview-box");
  
    uploadInput.addEventListener("change", function () {
      const file = uploadInput.files[0];
  
      if (file) {
        const reader = new FileReader();
  
        reader.onload = function (e) {
          previewBox.innerHTML = `<img src="${e.target.result}" alt="Uploaded Preview">`;
        };
  
        reader.readAsDataURL(file);
      } else {
        previewBox.innerHTML = "<p>No image selected yet.</p>";
      }
    });
  
    // === Show Modal on Upload ===
    const form = document.querySelector("form");
    form.addEventListener("submit", function () {
      const modal = document.getElementById("generated-modal");
      const imageBox = document.getElementById("modal-image-box");
  
      modal.style.display = "flex";
      imageBox.innerHTML = `
        <div id="loading-animation">
          <p style="color: #6b7280">Generating image...</p>
          <div class="spinner"></div>
        </div>
      `;
    });
  });
  
  // === Close Modal Functionality ===
  function closeModal() {
    const modal = document.getElementById("generated-modal");
    modal.style.display = "none";
  }
  