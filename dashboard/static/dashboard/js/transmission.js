// Get the modal element
const transmissionModal = document.getElementById('transmissionModal');
const closeTransmissionModal = document.getElementById('closeTransmissionModal');

// Function to show the modal
function showTransmissionModal() {
  transmissionModal.style.display = 'flex';
}

// Function to hide the modal and redirect to the correct URL
function hideTransmissionModalAndRedirect() {
  transmissionModal.style.display = 'none';
  // Redirect to the correct URL (make sure to use an absolute path)
  window.location.href = '/dashboard/transmission/';
}

// Handle "Enviar" button click
document.querySelector('.send-btn').addEventListener('click', function(event) {
  event.preventDefault();  // Prevent default form submission
  showTransmissionModal();  // Show modal when "Enviar" is clicked
});

// Handle modal "OK" button click
closeTransmissionModal.addEventListener('click', function() {
  hideTransmissionModalAndRedirect();  // Redirect after closing the modal
});
