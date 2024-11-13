document.addEventListener('DOMContentLoaded', function () {
    const deleteButtons = document.querySelectorAll('.delete-btn'); // Targets message delete buttons
    const modal = document.getElementById('deleteModal'); // Modal for delete confirmation
    const deleteForm = document.getElementById('deleteForm'); // Form inside the modal
    const cancelButton = document.querySelector('.cancel-btn'); // Cancel button inside modal
    const confirmButton = document.querySelector('.confirm-btn'); // Confirm button inside modal
  
    deleteButtons.forEach(button => {
      button.addEventListener('click', function () {
        const actionUrl = this.getAttribute('data-action-url'); // Get the delete URL for the message
        deleteForm.action = actionUrl; // Set the form action to the correct URL
        modal.style.display = 'flex'; // Show the modal
      });
    });
  
    // Close the modal when cancel button is clicked
    cancelButton.addEventListener('click', function () {
      closeModal();
    });
  
    // Submit the form when confirm button is clicked
    confirmButton.addEventListener('click', function () {
      deleteForm.submit(); // Submit the form to delete the message
    });
  
    // Close the modal when clicking outside of it
    window.onclick = function (event) {
      if (event.target === modal) {
        closeModal();
      }
    };
  
    // Function to close the modal
    function closeModal() {
      modal.style.display = 'none'; // Hide the modal
    }
  });