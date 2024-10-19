// Get the modal element
const messageModal = document.getElementById('messageModal');
const closeMessageModal = document.getElementById('closeMessageModal');

// Function to show the modal
function showMessageModal() {
  messageModal.style.display = 'flex';
}

// Function to hide the modal and redirect
function hideMessageModalAndRedirect() {
  messageModal.style.display = 'none';
  window.location.href = 'messages.html';
}

// Handle "Adicionar Produto" button click
document.querySelector('.submit-btn').addEventListener('click', function(event) {
  event.preventDefault(); 
  showMessageModal();
});

// Handle modal "OK" button click
closeMessageModal.addEventListener('click', function() {
  hideMessageModalAndRedirect();
});
