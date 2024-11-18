document.addEventListener('DOMContentLoaded', function() {
  // Get all required elements
  const deleteButtons = document.querySelectorAll('.delete-btn');
  const modal = document.getElementById('deleteModal');
  const deleteForm = document.getElementById('deleteForm');
  const cancelBtn = document.querySelector('.cancel-btn');
  let currentForm = null;

  // Function to open the modal
  function openModal(form) {
      modal.style.display = 'flex';
      currentForm = form;
      // Set the form's action to match the original form
      deleteForm.action = form.action;
  }

  // Function to close the modal
  function closeModal() {
      modal.style.display = 'none';
      currentForm = null;
  }

  // Add click event listeners to all delete buttons
  deleteButtons.forEach(button => {
      button.addEventListener('click', function(e) {
          e.preventDefault();
          // Get the parent form of the clicked button
          const form = this.closest('form');
          if (form) {
              openModal(form);
          }
      });
  });

  // Handle cancel button click
  cancelBtn.addEventListener('click', function(e) {
      e.preventDefault();
      closeModal();
  });

  // Handle modal confirm button click
  deleteForm.addEventListener('submit', function(e) {
      e.preventDefault();
      if (currentForm) {
          // Copy the CSRF token from the original form to the modal form
          const csrfToken = currentForm.querySelector('input[name="csrfmiddlewaretoken"]').value;
          const modalCsrfInput = this.querySelector('input[name="csrfmiddlewaretoken"]');
          modalCsrfInput.value = csrfToken;
          
          // Submit the form
          this.submit();
      }
  });

  // Close modal when clicking outside
  window.addEventListener('click', function(e) {
      if (e.target === modal) {
          closeModal();
      }
  });

  // Make closeModal function available globally
  window.closeModal = closeModal;
  window.openModal = function() {
      const form = document.getElementById('deleteFormTrigger');
      if (form) {
          openModal(form);
      }
  };

  // Optional: Add keyboard support for closing modal with Escape key
  document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && modal.style.display === 'flex') {
          closeModal();
      }
  });
});