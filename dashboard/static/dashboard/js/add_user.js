// Get the modal element
const userModal = document.getElementById('userModal');
const closeUserModal = document.getElementById('closeUserModal');

// Function to show the modal
function showUserModal() {
  userModal.style.display = 'flex';
}

// Function to hide the modal and redirect
function hideUserModalAndRedirect() {
  userModal.style.display = 'none';
  // Use Django's URL for redirection
  window.location.href = '/dashboard/users/';  // This is the correct URL for the users page in Django
}

// Handle form submission
document.querySelector('.user-form').addEventListener('submit', function(event) {
  event.preventDefault();  // Prevent the default form submission

  // Simulate form submission success (you can integrate an AJAX call if needed)
  showUserModal();
});

// Handle modal "OK" button click
closeUserModal.addEventListener('click', function() {
  hideUserModalAndRedirect();
});
