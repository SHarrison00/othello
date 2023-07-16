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
  // Add logic to send the row and col values to the backend
}