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

function displayMessage(message) {
  const messageBox = document.getElementById('message-box');
  messageBox.textContent = message;
  messageBox.style.visibility = 'visible';
}

function fetchAndDisplayGameOutcome() {
  fetch('/get_game_outcome')
    .then(response => response.json())
    .then(data => {
      displayMessage(data.outcome_message);
    })
    .catch(error => console.error('Error fetching game outcome:', error));
}

function handleUserMove(event) {
  const tdElement = event.target.closest('.cell');

  if (tdElement) {
    const row = parseInt(tdElement.dataset.row);
    const col = parseInt(tdElement.dataset.col);

    // Hide any previously displayed message
    document.getElementById('message-box').style.visibility = 'hidden';

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
        console.log('Response from backend:', data);
        updateGameBoard();

        if (data.game_over) {
          // Fetch/display outcome if game over
          fetchAndDisplayGameOutcome();
        } else {
          // Request Agent's move if game not over
          handleAgentMove();
        }
      })
      .catch(userError => {
        console.error('User Error:', userError);
      });
  } else {
    console.error('Invalid click, no parent <td> element found.');
  }
}

function handleAgentMove() {
  // Initially hide valid moves
  validMovesVisible = false; 

  displayMessage("OthelloAI is analysing...");

  setTimeout(() => {
    fetch('/agent_move', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    })
    .then(response => response.json())
    .then(data => {
      console.log('Response from backend:', data);
      updateGameBoard();

      if (data.game_over) {
        // Fetch and display the game outcome
        fetchAndDisplayGameOutcome();
      } else {
        if (data.agent_moved) {
          // If OthelloAI made a move
          if (data.user_has_moves) {
            // If user has valid moves
            validMovesVisible = true;
            document.getElementById('message-box').style.visibility = 'hidden';
          } else {
            // If user has no valid moves
            console.log("User has no valid moves, AI's turn again.");
            displayMessage("You have no valid moves. OthelloAI's turn.");

            // Schedule AI to move again after a delay
            setTimeout(handleAgentMove, 2000);
          }
        } else {
          // If OthelloAI had no valid moves
          if (!data.user_has_moves) {
            // If user also has no valid moves
            console.log("Neither AI nor user has valid moves. Game over.");

            // Fetch and display the game outcome
            fetchAndDisplayGameOutcome();
          } else {
            // If user has valid moves
            console.log("Agent had no valid move, user's turn again.");
            displayMessage("OthelloAI has no valid moves. Your turn.");

            // Show valid moves for  user
            validMovesVisible = true;
            updateGameBoard();
          }
        }
      }
    })
    .catch(agentError => {
      console.error('Agent Error:', agentError);
    });
  // Delay for AI's response
  }, 2000);
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