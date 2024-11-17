const editCategoryModal = document.getElementById("editCategoryModal");
const closeEditCategoryModal = document.getElementById(
  "closeEditCategoryModal"
);
const editCategoryForm = document.getElementById("editCategoryForm");
const editCategoryId = document.getElementById("editCategoryId");
const editCategoryName = document.getElementById("editCategoryName");
const editCategoryStatus = document.getElementById("editCategoryStatus");

const deleteCategoryModal = document.getElementById("deleteCategoryModal");
const closeDeleteCategoryModal = document.getElementById(
  "closeDeleteCategoryModal"
);
const deleteCategoryForm = document.getElementById("deleteCategoryForm");
const deleteCategoryId = document.getElementById("deleteCategoryId");

function hideEditCategoryModal() {
  editCategoryModal.style.display = "none";
}

function showEditCategoryModal(category) {
  editCategoryId.value = category.id;
  editCategoryName.value = category.name;
  editCategoryStatus.value = category.is_active === "Sim" ? "True" : "False";
  editCategoryForm.action = `/dashboard/dashboard/categories/edit/${category.id}/`;
  editCategoryModal.style.display = "flex";
}

document.querySelectorAll(".edit-btn").forEach((button) => {
  button.addEventListener("click", function (event) {
    const categoryRow = event.target.closest("tr");
    const categoryId = categoryRow.getAttribute("data-id");
    const categoryName = categoryRow.querySelector("td:first-child").innerText;
    const categoryStatus =
      categoryRow.querySelector("td:nth-child(2)").innerText;

    showEditCategoryModal({
      id: categoryId,
      name: categoryName,
      is_active: categoryStatus,
    });
  });
});

closeEditCategoryModal.addEventListener("click", hideEditCategoryModal);

editCategoryForm.addEventListener("submit", function (event) {
  hideEditCategoryModal();
});

window.addEventListener("click", function (event) {
  if (event.target === editCategoryModal) {
    hideEditCategoryModal();
  }
});

function hideDeleteCategoryModal() {
  deleteCategoryModal.style.display = "none";
}

function showDeleteCategoryModal(categoryId) {
  deleteCategoryId.value = categoryId;
  deleteCategoryForm.action = `/dashboard/dashboard/categories/delete/${categoryId}/`;
  deleteCategoryModal.style.display = "flex";
}

// Adicione os event listeners para os botões de delete
document.querySelectorAll(".delete-btn").forEach((button) => {
  button.addEventListener("click", function (event) {
    const categoryRow = event.target.closest("tr");
    const categoryId = categoryRow.getAttribute("data-id");
    showDeleteCategoryModal(categoryId);
  });
});

closeDeleteCategoryModal.addEventListener("click", hideDeleteCategoryModal);

deleteCategoryForm.addEventListener("submit", function (event) {
  hideDeleteCategoryModal();
});

window.addEventListener("click", function (event) {
  if (event.target === editCategoryModal) {
    hideEditCategoryModal();
  }
  if (event.target === deleteCategoryModal) {
    hideDeleteCategoryModal();
  }
});
