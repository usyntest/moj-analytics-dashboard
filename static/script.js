const submitButton = document.querySelector(".home-search-form-submit-button");

submitButton.addEventListener("click", (e) => {
  e.target.innerHTML = `Gathering Data <span class="loader"></span>`;
});
