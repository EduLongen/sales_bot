// Get the modal element
const productModal = document.getElementById('productModal');
const closeProductModal = document.getElementById('closeProductModal');

// Function to show the modal
function showProductModal() {
  productModal.style.display = 'flex';
}

// Function to hide the modal and redirect
function hideProductModalAndRedirect() {
  productModal.style.display = 'none';
  window.location.href = '/dashboard/products/';  // Redirect to products page
}

// Handle form submission
document.querySelector('.product-form').addEventListener('submit', function(event) {
  event.preventDefault();  // Prevent the default form submission

  // Simulate form submission success (you can integrate an AJAX call if needed)
  showProductModal();
});

// Handle modal "OK" button click
closeProductModal.addEventListener('click', function() {
  hideProductModalAndRedirect();
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
