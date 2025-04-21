document.addEventListener("DOMContentLoaded", function () {
    const popupContainer = document.getElementById("popupContainer");
    const form = document.getElementById("signupForm");
    const emailInput = document.getElementById("email");
    const nextBtn = document.getElementById("nextBtn");
    const backBtn = document.getElementById("backBtn");
    const step1 = document.getElementById("step1");
    const step2 = document.getElementById("step2");

    // Email validation on form submit
    if (form) {
        form.addEventListener("submit", function (event) {
            const email = emailInput.value.trim();

            if (!validateEmail(email)) {
                event.preventDefault(); // Stop form submission
                showPopup("Please enter a valid email ID", "error");
            }
        });
    }

    // Multi-step form navigation
    if (nextBtn && backBtn && step1 && step2) {
        // Move to Step 2
        nextBtn.addEventListener("click", function () {
            step1.style.display = "none";
            step2.style.display = "block";
        });

        // Move back to Step 1
        backBtn.addEventListener("click", function () {
            step1.style.display = "block";
            step2.style.display = "none";
        });

        // Detect "Enter" key on Step 1 fields
        step1.addEventListener("keypress", function (event) {
            if (event.key === "Enter") {
                event.preventDefault(); // Prevent form submission
                nextBtn.click(); // Move to Step 2
            }
        });

        // Detect "Enter" key on Step 2 fields
        step2.addEventListener("keypress", function (event) {
            if (event.key === "Enter") {
                event.preventDefault(); // Prevent default action
                form?.submit(); // Submit the form safely
            }
        });
    }

    // Function to validate email
    function validateEmail(email) {
        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return emailRegex.test(email);
    }

    // Function to create and auto-remove popups
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
});