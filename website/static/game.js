// Function to update the game board based on the received game state
function updateGameBoard(gameState) {
  for (let row = 0; row < 8; row++) {
    for (let col = 0; col < 8; col++) {
      const cell = gameState[row][col];
      const cellElement = document.querySelector(`.cell[data-row="${row}"][data-col="${col}"]`);

      if (cell === 'BLACK') {
        cellElement.innerHTML = '<div class="black-disc"></div>';
      } else if (cell === 'WHITE') {
        cellElement.innerHTML = '<div class="white-disc"></div>';
      } else if (cell === 'VALID') {
        cellElement.innerHTML = '';
      }
    }
  }
}

document.addEventListener('DOMContentLoaded', function () {
  // Add event listener to valid cells
  const validCells = document.querySelectorAll('.grey-disc');
  validCells.forEach(cell => {
    cell.addEventListener('click', handleClick);
  });

  // Click event handler
  function handleClick(event) {
    // Find the parent <td> element
    const tdElement = event.target.closest('.cell');

    // Check if a valid <td> element was found
    if (tdElement) {
      const row = parseInt(tdElement.dataset.row);
      const col = parseInt(tdElement.dataset.col);
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
        // After a successful move, update the game board
        updateGameState();

        // Make computer move

        // Update game state

        // etc...
      })
      .catch(error => {
        console.error('Error:', error);
      });
    } else {
      console.error('Invalid click, no parent <td> element found.');
    }
  }

  // Function to fetch and update the game state from the server
  function updateGameState() {
    fetch('/get_game_state')
        .then(response => response.json())
        .then(data => {
          updateGameBoard(data.game_state);
        })
        .catch(error => {
          console.error('Error fetching game state:', error);
        });
  }
});