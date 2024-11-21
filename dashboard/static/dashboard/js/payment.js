// Get modal and buttons
const deleteModal = document.getElementById('deleteModal');
const confirmDeleteButton = document.getElementById('confirmDelete');
const cancelDeleteButton = document.getElementById('cancelDelete');

// Function to show the delete modal
function showDeleteModal(formElement) {
  deleteModal.style.display = 'flex';

  confirmDeleteButton.onclick = function () {
    formElement.submit(); // Submit the form with POST method
  };
}

// Function to hide the delete modal
function hideDeleteModal() {
  deleteModal.style.display = 'none';
}

// Attach event listeners to delete buttons
document.querySelectorAll('.delete-btn').forEach(function (button) {
  button.addEventListener('click', function (event) {
    event.preventDefault(); // Prevent default button action
    const formElement = this.closest('form'); // Get the form element
    showDeleteModal(formElement); // Pass the form element to the modal
  });
});

// Cancel button hides the modal
cancelDeleteButton.addEventListener('click', hideDeleteModal);

// Close modal on outside click
deleteModal.addEventListener('click', function (event) {
  if (event.target === deleteModal) hideDeleteModal();
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