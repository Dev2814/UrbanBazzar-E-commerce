document.addEventListener("DOMContentLoaded", function () {
  // Update form action URL and set the hidden field for secondary address
  document.querySelectorAll(".btn-add-address").forEach(function (button) {
    button.addEventListener("click", function () {
      var isSecondary = this.getAttribute("data-secondary") === "true";
      var formAction = isSecondary
        ? "{% url 'users:add_secondary_address' %}"
        : "{% url 'users:add_primary_address' %}";
      document.getElementById("addressForm").action = formAction;
      document.getElementById("is_secondary").value = isSecondary;
    });
  });

  // Handle UPI input visibility
  const upiRadio = document.getElementById("upiRadio");
  const codRadio = document.querySelector(
    "input[name='payment_method'][value='COD']"
  );
  const upiInput = document.getElementById("upiInput");

  function toggleUpiField() {
    if (upiRadio && upiRadio.checked) {
      upiInput.style.display = "block";
    } else {
      upiInput.style.display = "none";
    }
  }

  if (upiRadio) upiRadio.addEventListener("change", toggleUpiField);
  if (codRadio) codRadio.addEventListener("change", toggleUpiField);

  toggleUpiField(); // Initialize visibility on page load
});
