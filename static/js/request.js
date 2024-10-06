// Get the table element
var table = document.getElementById("dataTable");

// Initialize an array to store the table data
var jsonData = [];

// Iterate through each row in the table
for (var i = 1; i < table.rows.length; i++) {  // Start from 1 to skip the header row
    var row = table.rows[i];
    
    // Create an object to store the row data
    var rowData = {
        project: row.cells[0].innerText,
        domain: row.cells[1].innerText,
        status: row.cells[2].innerText,
        uploadDate: row.cells[3].innerText,
        urgency: row.cells[4].innerText
    };
    
    // Add the row data to the array
    jsonData.push(rowData);
}

// Convert the array to JSON string
var data = JSON.stringify(jsonData);

const rowsPerPageOptions = [10, 25, 50, 100];
let currentPage = 1;
let rowsPerPage = rowsPerPageOptions[0];
let filteredData = data;

// Function to render the table rows
function renderTableRows() {
    const tableBody = document.getElementById('tableBody');
    tableBody.innerHTML = '';

    const startIdx = (currentPage - 1) * rowsPerPage;
    const endIdx = startIdx + rowsPerPage;
    const visibleData = filteredData.slice(startIdx, endIdx);

    for (let i = 0; i < visibleData.length; i++) {
        const rowData = visibleData[i];
        const row = document.createElement('tr');
        row.innerHTML = `
        <td>${rowData.project}</td>
        <td>${rowData.domain}</td>
        <td>${rowData.status}</td>
        <td>${rowData.uploadDate}</td>
        <td>${rowData.urgency}</td>
      `;
        tableBody.appendChild(row);
    }
}

// Function to update pagination buttons and page info
function updatePagination() {
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const pageInfo = document.getElementById('pageInfo');

    const totalPages = Math.ceil(filteredData.length / rowsPerPage);

    prevBtn.disabled = currentPage === 1;
    nextBtn.disabled = currentPage === totalPages;

    pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;
}

// Function to handle search input
function handleSearch() {
    const searchInput = document.getElementById('searchInput');
    const searchTerms = searchInput.value.toLowerCase().split(',').map(term => term.trim());

    filteredData = data.filter((row) => {
        const isStatusMatch = document.querySelector('.nav-button.active').dataset.status === 'all' ||
            document.querySelector('.nav-button.active').dataset.status === row.status.toLowerCase();

        return isStatusMatch && searchTerms.every((term) => {
            return (
                row.project.toLowerCase().includes(term) ||
                row.domain.toLowerCase().includes(term) ||
                row.status.toLowerCase().includes(term) ||
                row.uploadDate.toLowerCase().includes(term) ||
                row.projectType.toLowerCase().includes(term) ||
                row.urgency.toLowerCase().includes(term)
            );
        });
    });

    currentPage = 1;
    renderTableRows();
    updatePagination();
}



// Function to handle rows per page selection
function handleRowsPerPage() {
    const selectElement = document.getElementById('rowsPerPage');
    rowsPerPage = parseInt(selectElement.value);

    currentPage = 1;
    renderTableRows();
    updatePagination();
}

// Function to navigate to previous page
function goToPrevPage() {
    if (currentPage > 1) {
        currentPage--;
        renderTableRows();
        updatePagination();
    }
}

// Function to navigate to next page
function goToNextPage() {
    const totalPages = Math.ceil(filteredData.length / rowsPerPage);
    if (currentPage < totalPages) {
        currentPage++;
        renderTableRows();
        updatePagination();
    }
}

// Function to filter table data based on status
function filterData(status) {
    if (status === 'all') {
        filteredData = data;
    } else {
        filteredData = data.filter(row => row.status.toLowerCase() === status);
    }

    currentPage = 1;
    renderTableRows();
    updatePagination();
}

// Attach event listeners
document.getElementById('searchInput').addEventListener('input', handleSearch);
document.getElementById('rowsPerPage').addEventListener('change', handleRowsPerPage);
document.getElementById('prevBtn').addEventListener('click', goToPrevPage);
document.getElementById('nextBtn').addEventListener('click', goToNextPage);

const navButtons = document.querySelectorAll('.nav-button');
navButtons.forEach((button) => {
    button.addEventListener('click', () => {
        const status = button.dataset.status;
        navButtons.forEach((btn) => btn.classList.remove('active'));
        button.classList.add('active');
        filterData(status);
    });
});

// Initial rendering
renderTableRows();
updatePagination();
