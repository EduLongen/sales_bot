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
