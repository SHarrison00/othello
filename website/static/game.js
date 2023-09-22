// Flag to indicate whether valid moves are visible
let validMovesVisible = true;

// Function to update the game board based on the received game state
function updateGameBoard() {
  // AJAX request to backend for game state
  fetch('/get_game_state')
    .then(response => response.json())
    .then(data => {
      const gameState = data.game_state;

      // Update board to reflect the updated state
      for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
          const cell = gameState[row][col];
          const cellElement = document.querySelector(`.cell[data-row="${row}"][data-col="${col}"]`);

          if (cell === 'BLACK') {
            cellElement.innerHTML = '<div class="black-disc"></div>';
          } else if (cell === 'WHITE') {
            cellElement.innerHTML = '<div class="white-disc"></div>';
          } else if (cell === 'VALID') {
            if (validMovesVisible) {
              cellElement.innerHTML = '<div class="grey-disc"></div>';
            } else {
              cellElement.innerHTML = '';
            }
          } else {
            cellElement.innerHTML = '';
          }
        }
      }
    })
    .catch(error => {
      console.error('Error fetching game state:', error);
    });
}

// Click event handler for User's move
function handleUserMove(event) {
  const tdElement = event.target.closest('.cell');

  if (tdElement) {
    const row = parseInt(tdElement.dataset.row);
    const col = parseInt(tdElement.dataset.col);

    // AJAX request to backend for User's move
    fetch('/user_move', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ row, col }),
    })
      .then(response => response.json())
      .then(data => {
        updateGameBoard();
        
        // Proceed to Agent's move
        handleAgentMove();
      })
      .catch(userError => {
        console.error('User Error:', userError);
      });
  } else {
    console.error('Invalid click, no parent <td> element found.');
  }
}

function handleAgentMove() {
  // Hide Agent's valid moves
  validMovesVisible = false;

  // Introduce 1.5s delay
  setTimeout(() => {
    // AJAX request to backend for Agent's move
    fetch('/agent_move', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then(response => response.json())
      .then(data => {
        updateGameBoard();
        validMovesVisible = true;
      })
      .catch(agentError => {
        console.error('Agent Error:', agentError);
      });
  }, 1500); // 1.5s delay
}

document.addEventListener('DOMContentLoaded', function () {
  // Attach a single event listener to a parent element (e.g., the table)
  const gameTable = document.querySelector('.game-board');
  gameTable.addEventListener('click', function (event) {
    // Check if the clicked element or any of its parents have the .grey-disc class
    if (event.target.closest('.grey-disc')) {
      handleUserMove(event);
    }
  });

  // If the user is playing as "white", the agent should make the first move
  if (userColor === 'WHITE') {
    console.log("User selected WHITE");
    validMovesVisible = false;
    updateGameBoard();
    setTimeout(() => {
      console.log("Agent is making the first move");
      handleAgentMove();
    }, 100);
  }
});