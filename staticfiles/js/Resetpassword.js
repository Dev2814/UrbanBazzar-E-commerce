document.addEventListener("DOMContentLoaded", function () {
    const popupContainer = document.getElementById("popupContainer");

    // Remove existing popups after 3 seconds
    const existingPopups = document.querySelectorAll(".popup");
    existingPopups.forEach(popup => {
        setTimeout(() => {
            popup.classList.add("slide-up");
            setTimeout(() => popup.remove(), 500);
        }, 3000);
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
});
