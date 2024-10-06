
// Call the function on page load
function blinkEmployeeList() {
  var employeeList = document.querySelector(".employee-list");
  employeeList.classList.add("blink-container");
  setTimeout(function() {
    employeeList.classList.remove("blink-container");
  }, 1000); // Duration of the blinking effect in milliseconds
}
// function showEmployeeDetails(row) {
  
//   // Show the offcanvas sidebar
//   var offcanvas = new bootstrap.Offcanvas(document.getElementById('sidebarOffcanvas'));
//   offcanvas.show();
// }
      // Add event listener to the Edit button
  var editButton = document.querySelector('.edit-button');
  editButton.addEventListener('click', showEditNotification);

  // Function to show the edit notification
  function showEditNotification() {
    $('#editEmployeeModal').modal('show');
  }

  // // Function to handle editing an existing employee
  // function editEmployee() {
  //   // Add your code to handle editing an existing employee here
  //   // For example, you can redirect to a specific page for editing employee details
  //   window.location.href = 'edit_employee.html';
  // }

  // // Function to handle creating a new employee
  // function createEmployee() {
  //   // Add your code to handle creating a new employee here
  //   // For example, you can redirect to a specific page for creating a new employee
  //   window.location.href = 'create_employee.html';
  // }
  // Function to handle creating a new employee
  function createEmployee() {
    // Add your code to handle creating a new employee here
    // For example, you can redirect to a specific page for creating a new employee
    window.location.href = 'create_employee.html';
  }