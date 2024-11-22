// Get the message modal elements
const messageModal = document.getElementById('messageModal');
const closeMessageModal = document.getElementById('closeMessageModal');

// Function to show the message modal
function showMessageModal() {
  messageModal.style.display = 'flex';
}

// Function to hide the message modal and redirect to the messages page
function hideMessageModalAndRedirect() {
  messageModal.style.display = 'none';
  window.location.href = '/dashboard/messages/';  // Corrected URL for messages page
}

// Handle "Adicionar Mensagem" button click
document.querySelector('.add-message-btn').addEventListener('click', function(event) {
  event.preventDefault(); 
  showMessageModal();
});

// Handle modal "OK" button click for message modal
closeMessageModal.addEventListener('click', function() {
  hideMessageModalAndRedirect();
});
