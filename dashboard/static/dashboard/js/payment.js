// Get the modal element
const paymentModal = document.getElementById('paymentModal');
const closePaymentModal = document.getElementById('closePaymentModal');

// Function to show the modal
function showPaymentModal() {
  paymentModal.style.display = 'flex';
}

// Function to hide the modal and redirect
function hidePaymentModalAndRedirect() {
  paymentModal.style.display = 'none';
  window.location.href = '/dashboard/payment/';
}

// Handle "Adicionar Pagamento" button click
document.querySelector('.submit-btn').addEventListener('click', function(event) {
  event.preventDefault(); 
  showPaymentModal();
});

// Handle modal "OK" button click
closePaymentModal.addEventListener('click', function() {
  hidePaymentModalAndRedirect();
});
