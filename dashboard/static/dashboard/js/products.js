const editProductModal = document.querySelector(".modal-overlay");
const editProductForm = document.getElementById("editProductForm");
const editProductId = document.getElementById("editProductId");
const editProductName = document.getElementById("editProductName");
const editProductPrice = document.getElementById("editProductPrice");
const editProductStatus = document.getElementById("editProductStatus");
const editImageUrl = document.getElementById("editImageUrl");
const editDescription = document.getElementById("editDescription");
const editCategory = document.getElementById("editCategory");
const cancelButton = document.querySelector(".cancel-btn");
const confirmButton = document.querySelector(".confirm-btn");

function hideEditProductModal() {
  editProductModal.style.display = "none";
}

function showEditProductModal(product) {
  console.log("Opening modal with product:", product); // Verifique os dados
  editProductId.value = product.id;
  editProductName.value = product.name;
  editImageUrl.value = product.image_url;
  if (editCategory && editCategory.options) {
    for (let i = 0; i < editCategory.options.length; i++) {
      if (editCategory.options[i].value == product.category_id) {
        editCategory.selectedIndex = i;
        break;
      }
    }
  }
  editDescription.value = product.description || "";
  editProductPrice.value = product.price;
  console.log("Product ", product.is_active);
  editProductStatus.value = product.is_active === true ? "True" : "False";
  editProductForm.action = `/dashboard/products/edit/${product.id}/`;
  editProductModal.style.display = "flex";
}

document.addEventListener("DOMContentLoaded", () => {
  const editButtons = document.querySelectorAll(".edit-btn");
  console.log(`Found ${editButtons.length} edit buttons`);

  editButtons.forEach((button) => {
    button.addEventListener("click", function (event) {
      console.log("Edit button clicked");
      const productRow = event.target.closest("tr");

      console.log("Product row", productRow.dataset);
      showEditProductModal({
        id: productRow.dataset.id,
        name: productRow.dataset.name,
        category_id: productRow.dataset.category,
        price: productRow.dataset.price,
        is_active: productRow.dataset.active === "true", // Use lowercase "true"
        image_url: productRow.dataset.imageUrl,
        description: productRow.dataset.description,
      });
    });
  });

 // Close the modal when cancel button is clicked
 cancelButton.addEventListener('click', function () {
  closeModal();
});

  
  confirmButton.addEventListener("click", function (event) {
    hideEditProductModal();
  });

});

// Messages Timer: Hide messages after 5 seconds
document.addEventListener("DOMContentLoaded", function () {
  const messagesContainer = document.querySelector(".messages-container");
  if (messagesContainer) {
    setTimeout(() => {
      messagesContainer.style.display = "none";
    }, 5000);
  }
});
