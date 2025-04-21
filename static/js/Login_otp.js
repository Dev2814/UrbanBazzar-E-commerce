document.addEventListener("DOMContentLoaded", function () {
    const otpInputs = document.querySelectorAll(".input-field input");
    const popupContainer = document.getElementById("popupContainer");
    const form = document.getElementById("otpForm");
  
    otpInputs.forEach((input, index) => {
      // Move focus to the next input field if the current input is filled
      input.addEventListener("input", function () {
        if (input.value.length === input.maxLength) {
          const nextInput = otpInputs[index + 1];
          if (nextInput) {
            nextInput.focus();
          }
        }
      });
  
      // Handle backspace key press to move focus to the previous input field
      input.addEventListener("keydown", function (event) {
        if (event.key === "Backspace" && input.value === "") {
          const previousInput = otpInputs[index - 1];
          if (previousInput) {
            previousInput.focus();
            previousInput.value = ""; // Clear the previous input value
          }
        }
      });
    });
  
    // Function to create popups
    function showPopup(message, type) {
      const popup = document.createElement("div");
      popup.className = `popup ${type}`;
      popup.innerHTML = message;
      popupContainer.appendChild(popup);
  
      setTimeout(() => {
        popup.classList.add("slide-up");
        setTimeout(() => popup.remove(), 500);
      }, 3000);
    }
  
    // Remove existing popups after 3 seconds (even success messages)
    const existingPopups = document.querySelectorAll(".popup");
    existingPopups.forEach(popup => {
      setTimeout(() => {
        popup.classList.add("slide-up");
        setTimeout(() => popup.remove(), 500);
      }, 3000);
    });
  
    // Form submit event listener
    form.addEventListener("submit", function (event) {
      event.preventDefault(); // Prevent form submission
  
      // Check if all inputs are filled
      let allFilled = true;
      otpInputs.forEach((input) => {
        if (!input.value) {
          allFilled = false;
          input.focus();
          return;
        }
      });
  
      if (allFilled) {
        showPopup("Verifying OTP...", "success");
        form.submit(); // Allow form submission
      } else {
        showPopup("Please fill all OTP fields.", "error");
      }
    });
  });