const editProductModal = document.getElementById("editProductModal");
const closeEditProductModal = document.getElementById("closeEditProductModal");
const editProductForm = document.getElementById("editProductForm");
const editProductId = document.getElementById("editProductId");
const editProductName = document.getElementById("editProductName");
const editProductPrice = document.getElementById("editProductPrice");
const editProductStatus = document.getElementById("editProductStatus");

function hideEditProductModal() {
  editProductModal.style.display = "none";
}

function showEditProductModal(product) {
  editProductId.value = product.id;
  editProductName.value = product.name;
  const editProductPrice = parseFloat(productRow.querySelector("td:nth-child(3)").innerText.replace(',', '.'));
  editProductStatus.value = product.is_active === true || product.is_active === "Sim" ? "True" : "False";
  editProductForm.action = `/dashboard/products/edit/${product.id}/`;
  editProductModal.style.display = "flex";
}

document.querySelectorAll(".edit-btn").forEach((button) => {
  button.addEventListener("click", function (event) {
    const productRow = event.target.closest("tr");
    const productId = productRow.getAttribute("data-id");
    const productName = productRow.querySelector("td:first-child").innerText;
    const productPrice = productRow.querySelector("td:nth-child(3)").innerText;
    const productStatus = productRow.querySelector("td:nth-child(4)").innerText;

    showEditProductModal({
      id: productId,
      name: productName,
      price: productPrice,
      is_active: productStatus === "Sim"
    });
  });
});

closeEditProductModal.addEventListener("click", hideEditProductModal);

editProductForm.addEventListener("submit", function (event) {
  // Prevent default form submission to allow AJAX if needed
  // event.preventDefault();
  
  // Optionally add form validation here
  hideEditProductModal();
});

window.addEventListener("click", function (event) {
  if (event.target === editProductModal) {
    hideEditProductModal();
  }
});