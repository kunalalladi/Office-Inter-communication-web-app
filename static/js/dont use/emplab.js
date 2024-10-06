function searchEmployee() {
  var input, filter, table, tbody, tr, td, i, txtValue;
  input = document.getElementById("searchInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("employeeTableBody");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, hide those that don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td");
    for (var j = 0; j < td.length; j++) {
      var cell = td[j];
      if (cell) {
        txtValue = cell.textContent || cell.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
          break; // Break the inner loop if a match is found
        } else {
          tr[i].style.display = "none";
        }
      }
    }
  }
}
 // Function to update the total number of employees
 function updateTotalNumber() {
  var totalNumber = document.getElementById("employeeTableBody").rows.length;
  document.getElementById("totalNumber").textContent = totalNumber.toString();
}
function updateEmployeeCount() {
  // Get the table body element from online.html
  var tableBody = window.opener.document.getElementById("employeeTableBody");

  // Count the number of rows in the table
  var employeeCount = tableBody.getElementsByTagName("tr").length;

  // Update the onlineNumber element in emplab.html
  var onlineNumberElement = document.getElementById("onlineNumber");
  if (onlineNumberElement) {
    onlineNumberElement.textContent = employeeCount;
  }
}

// Call the updateEmployeeCount function when the page loads
window.addEventListener("DOMContentLoaded", function() {
  updateEmployeeCount();
});

// Call the function on page load
window.onload = updateTotalNumber;
function blinkEmployeeList() {
  var employeeList = document.querySelector(".employee-list");
  employeeList.classList.add("blink-container");
  setTimeout(function() {
    employeeList.classList.remove("blink-container");
  }, 1000); // Duration of the blinking effect in milliseconds
}
function showEmployeeDetails(row) {
  // Get the employee details from the clicked row
  var id = row.cells[0].innerText;
  var name = row.cells[1].innerText;
  var dept = row.cells[2].innerText;
  var designation = row.cells[3].innerText;
  var domain = row.cells[4].innerText;

  // Set the employee details in the offcanvas sidebar
  document.getElementById('sidebarOffcanvasLabel').innerText = 'Details';
  document.getElementById('sidebarOffcanvasId').textContent = id;
  document.getElementById('sidebarOffcanvasName').textContent = name;
  document.getElementById('sidebarOffcanvasDept').textContent = dept;
  document.getElementById('sidebarOffcanvasDesignation').textContent = designation;
  document.getElementById('sidebarOffcanvasDomain').textContent = domain;

  // Show the offcanvas sidebar
  var offcanvas = new bootstrap.Offcanvas(document.getElementById('sidebarOffcanvas'));
  offcanvas.show();
}
window.addEventListener('DOMContentLoaded', function() {
  var projectNumber = document.getElementById('projectNumber');
  var projectCards = document.getElementsByClassName('project-card');
  projectNumber.textContent = projectCards.length;
});
fetch('project.html')
      .then(response => response.text())
      .then(data => {
        // Parse the HTML response
        const parser = new DOMParser();
        const htmlDoc = parser.parseFromString(data, 'text/html');

        // Get the count of project cards
        const projectCount = htmlDoc.getElementsByClassName('card custom-card').length;

        // Update the projectNumber element in the current HTML file
        const projectNumberElement = document.getElementById('projectNumber');
        projectNumberElement.textContent = projectCount;
      })
      .catch(error => console.error('Error fetching project.html:', error));
      // Add event listener to the Edit button
  var editButton = document.querySelector('.edit-button');
  editButton.addEventListener('click', showEditNotification);

  // Function to show the edit notification
  function showEditNotification() {
    $('#editEmployeeModal').modal('show');
  }

  // Function to handle editing an existing employee
  function editEmployee() {
    // Add your code to handle editing an existing employee here
    // For example, you can redirect to a specific page for editing employee details
    window.location.href = 'edit_employee.html';
  }

  // Function to handle creating a new employee
  function createEmployee() {
    // Add your code to handle creating a new employee here
    // For example, you can redirect to a specific page for creating a new employee
    window.location.href = 'create_employee.html';
  }