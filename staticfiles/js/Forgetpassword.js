document.addEventListener("DOMContentLoaded", function () {
    const popupContainer = document.getElementById("popupContainer");
    const form = document.getElementById("ForgetForm");
    const emailInput = document.getElementById("email");

    // Remove existing popups after 3 seconds
    const existingPopups = document.querySelectorAll(".popup");
    existingPopups.forEach(popup => {
        setTimeout(() => {
            popup.classList.add("slide-up");
            setTimeout(() => popup.remove(), 500);
        }, 3000);
    });

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

    // Function to validate email
    function validateEmail(email) {
        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return emailRegex.test(email);
    }

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
});
