// Get the modal element
const categoryModal = document.getElementById("categoryModal");
const closeCategoryModal = document.getElementById("closeCategoryModal");

// Function to show the modal
function showCategoryModal() {
  categoryModal.style.display = "flex";
}

// Function to hide the modal and redirect
function hideCategoryModalAndRedirect() {
  categoryModal.style.display = "none";
  window.location.href = "/dashboard/categories/"; // Ensure this points to the correct URL
}

// Handle form submission (when the "Adicionar Categoria" button is clicked)
document
  .querySelector(".add-category-btn")
  .addEventListener("click", function (event) {
    // Allow the form to submit normally to the backend
    showCategoryModal(); // Show modal before form submission
  });

// Handle modal "OK" button click
closeCategoryModal.addEventListener("click", function () {
  hideCategoryModalAndRedirect(); // Hide modal and redirect to the categories page
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
