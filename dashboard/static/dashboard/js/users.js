document.addEventListener('DOMContentLoaded', function () {
  const deleteButtons = document.querySelectorAll('.delete-btn');
  const modal = document.getElementById('deleteModal');
  const deleteForm = document.getElementById('deleteForm');
  const cancelButton = document.querySelector('.cancel-btn');
  const confirmButton = document.querySelector('.confirm-btn');

  // Show the modal and set form action URL when delete button is clicked
  deleteButtons.forEach(button => {
    button.addEventListener('click', function () {
      const actionUrl = this.getAttribute('data-action-url');
      deleteForm.action = actionUrl;
      modal.style.display = 'flex';  // Use 'flex' to center align with modal styles
    });
  });

  // Close the modal when cancel button is clicked
  cancelButton.addEventListener('click', function () {
    closeModal();
  });

  // Submit the form when confirm button is clicked
  confirmButton.addEventListener('click', function () {
    deleteForm.submit();
  });

  // Close the modal when clicking outside of it
  window.onclick = function (event) {
    if (event.target === modal) {
      closeModal();
    }
  };

  // Function to close the modal
  function closeModal() {
    modal.style.display = 'none';
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
