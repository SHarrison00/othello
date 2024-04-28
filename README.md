# OthelloAI WebApp

## Project Description

An online implementation of the classic Othello board game, featuring an AI opponent driven by the Minimax algorithm to compete with. For an in-depth explanation into the AI's functioning, refer to the project blog.

Website Preview:

![annotated_website](https://github.com/SHarrison00/othello/assets/86479780/8f1b2f0b-4ed1-4bd9-b2b3-75ac78363d47 "Website Preview: Play against OthelloAI.")

## How It Works

OthelloAI uses Python and Flask for its back-end, handling game logic and AI opponent operations. On the front-end, it employs AJAX requests to facilitate communication with the server, allowing players to make moves and play against OthelloAI.

## Links

- [Read the blog.](https://drive.google.com/file/d/1HXUY4hVqSeLwTT3QzbWTIvazhXH26HTF/view?usp=sharing)
- [Play OthelloAI.](https://othelloai.onrender.com)

## Repository Contents

Here's a quick overview of what you'll find in this repository:

- **Source Code:** The `src` folder is where you'll find the core code for implementing the Othello game logic and AI decision-making processes.

- **Testing:** In the `tests` folder, you'll find comprehensive tests to ensure everything works smoothly. To run tests, use the command `python -m tests.test` from the root directory.

- **AI Experimentation:** Explore AI functionality in the `src/experiments` folder, including Minimax algorithm move-time analysis and heuristic insights for Othello.
