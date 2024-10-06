// JavaScript code
var recipientDropdown = document.getElementById("recipient");
var officeDropdown = document.getElementById("office-dropdown");

recipientDropdown.addEventListener("change", function() {
  if (this.value === "select-office") {
    officeDropdown.style.display = "block";
  } else {
    officeDropdown.style.display = "none";
  }
});
