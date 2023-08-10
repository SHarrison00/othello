// Add event listener to valid cells
const validCells = document.querySelectorAll('.grey-disc');
validCells.forEach(cell => {
  cell.addEventListener('click', handleClick);
});

// Click event handler
function handleClick(event) {
  const row = parseInt(event.target.dataset.row);
  const col = parseInt(event.target.dataset.col);
  console.log('Clicked valid cell at (row, col): (', row, ',', col, ')');

  // Send AJAX request to backend
  fetch('/make_move', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ row, col }), // Send row and col as JSON data
  })
  .then(response => response.json())
  .then(data => {
    console.log('Response from backend:', data);
    // Add logic here to update the frontend game board based on the response
  })
  .catch(error => {
    console.error('Error:', error);
  });
}