const editCategoryModal = document.getElementById("editCategoryModal");
const editCategoryForm = document.getElementById("editCategoryForm");
const editCategoryId = document.getElementById("editCategoryId");
const editCategoryName = document.getElementById("editCategoryName");
const editCategoryStatus = document.getElementById("editCategoryStatus");
const cancelButton = document.querySelector('.cancel-btn');
const confirmButton = document.querySelector('.confirm-btn');

function hideEditCategoryModal() {
  editCategoryModal.style.display = "none";
}

function showEditCategoryModal(category) {
  editCategoryId.value = category.id;
  editCategoryName.value = category.name;
  editCategoryStatus.value = category.is_active === "Sim" ? "True" : "False";
  editCategoryForm.action = `/dashboard/categories/edit/${category.id}/`;
  editCategoryModal.style.display = "flex";
}

document.querySelectorAll(".edit-btn").forEach((button) => {
  button.addEventListener("click", function (event) {
    const categoryRow = event.target.closest("tr");
    const categoryId = categoryRow.getAttribute("data-id");
    const categoryName = categoryRow.querySelector("td:first-child").innerText;
    const categoryStatus =
      categoryRow.querySelector("td:nth-child(2)").innerText;

    showEditCategoryModal({
      id: categoryId,
      name: categoryName,
      is_active: categoryStatus,
    });
  });
});

// Close the modal when cancel button is clicked
cancelButton.addEventListener('click', function (event) {
  event.preventDefault();
  hideEditCategoryModal();
});

editCategoryForm.addEventListener("submit", function (event) {
  hideEditCategoryModal();
});

window.addEventListener("click", function (event) {
  if (event.target === editCategoryModal) {
    hideEditCategoryModal();
  }
});

// Messages Timer: Hide messages after 5 seconds
document.addEventListener('DOMContentLoaded', function () {
  const messagesContainer = document.querySelector('.messages-container');
  if (messagesContainer) {
    setTimeout(() => {
      messagesContainer.style.display = 'none';
    }, 5000);
  }
});