document.addEventListener("DOMContentLoaded", function () {
  const addBtn = document.getElementById("add-image-btn");
  const container = document.getElementById("image-formset-container");
  const totalForms = document.getElementById("id_form-TOTAL_FORMS");

  addBtn.addEventListener("click", function () {
    const currentFormCount = parseInt(totalForms.value);
    const firstForm = container.children[0];
    const newForm = firstForm.cloneNode(true);

    // Update attributes
    const input = newForm.querySelector("input");
    const oldName = input.name;
    const oldId = input.id;

    input.name = oldName.replace(/form-(\d+)/, `form-${currentFormCount}`);
    input.id = oldId.replace(/form-(\d+)/, `form-${currentFormCount}`);
    input.value = "";

    // Remove file info if exists
    const fileInfo = newForm.querySelector("p");
    if (fileInfo) fileInfo.remove();

    container.appendChild(newForm);
    totalForms.value = currentFormCount + 1;
  });
});
