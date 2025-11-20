Tic-Tac-Toe AI (Python)
=======================

A clean and minimalistic Python implementation of Tic-Tac-Toe featuring an unbeatable AI powered by the Minimax algorithm. The project is designed as a simple, college-level application that demonstrates clear code organization, turn-based game logic, and a classic recursive AI strategy.


Features
--------
• Human vs Human mode  
• Human vs AI mode (Minimax – impossible to beat)  
• Pure Python implementation, no external libraries  
• Modular and easy-to-read code structure  
• Clean separation between game logic, AI logic, and UI  


Project Structure
-----------------
tic_tac_toe/
    main.py          – Handles the game loop and player interaction  
    GameEngine.py    – Board representation, move handling, win detection  
    ai.py            – Minimax algorithm and AI move selection  
    utils.py         – Optional helper functions  
    README.txt       – Project documentation


How to Run
----------
1. Ensure Python 3 is installed.  
2. Clone or download the project.  
3. Open a terminal in the project directory.  
4. Run the game with:

    python3 main.py


How the AI Works
----------------
The AI uses the Minimax algorithm, a classic recursive search strategy that evaluates all possible future game states. Each board state receives an evaluation:

• +1  – AI victory  
• -1  – Human victory  
•  0  – Draw or neutral position  

By simulating all possible moves, Minimax ensures the AI always selects the optimal outcome. This approach makes the AI unbeatable while keeping the implementation compact and educational.


