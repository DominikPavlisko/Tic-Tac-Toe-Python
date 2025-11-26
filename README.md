# 🎮 Tic-Tac-Toe Python

A sophisticated Python implementation of Tic-Tac-Toe featuring an unbeatable AI powered by the Minimax algorithm, with support for both local and network-based multiplayer gameplay. Built with clean, modular code architecture and an intuitive GUI interface.

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)

---

## ✨ Features

- **🤖 Unbeatable AI** - Minimax algorithm ensures optimal gameplay
- **👥 Multiple Game Modes:**
  - Local Player vs Player (GUI)
  - Local Player vs AI
  - Network Player vs Player (LAN multiplayer)
  - Network Player vs AI (LAN with AI opponent)
- **🎨 Graphical User Interface** - Built with tkinter for smooth gameplay
- **🌐 Network Multiplayer** - Play over LAN with automatic server/client setup
- **📦 Zero External Dependencies** - Pure Python implementation (uses only standard library)
- **🏗️ Clean Architecture** - Modular design with separation of concerns

---

## 📋 Prerequisites

- **Python 3.x** or higher
- No external libraries required - uses Python's built-in modules:
  - `tkinter` (for GUI - usually comes pre-installed with Python)
  - `socket` (for network functionality)
  - `json` (for data serialization)
  - `threading` (for concurrent operations)

---

## 📁 Project Structure

```
Tic-Tac-Toe-Python/
├── main.py           # Main entry point with network server/client and GUI
├── GameEngine.py     # Core game logic, board state, win detection
├── AIEngine.py       # Minimax AI algorithm implementation
├── GUI.py            # Standalone GUI component
└── README.md         # Project documentation
```

### Module Descriptions

| File | Description |
|------|-------------|
| `main.py` | Network-enabled game with automatic server/client detection, supports both PvP and PvAI modes over LAN |
| `GameEngine.py` | Game state management, move validation, winner detection, and board operations |
| `AIEngine.py` | Minimax algorithm implementation for unbeatable AI opponent |
| `GUI.py` | Tkinter-based graphical interface for local gameplay (basic version) |

---

## 🚀 How to Run

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/DominikPavlisko/Tic-Tac-Toe-Python.git
cd Tic-Tac-Toe-Python
```

### 2️⃣ Run the Game

```bash
python3 main.py
```

### 🎮 Game Modes

When you run `main.py`, the application automatically:

1. **Checks for existing server** on `127.0.0.1:5000`
2. **If server exists**: Connects as a client
3. **If no server**: Starts a new server and prompts for mode selection:
   - **Option 1 - PvP**: Two players over network (both human)
   - **Option 2 - PvAI**: One player vs AI opponent

#### Local Network Multiplayer Setup

To play over LAN with another player:

1. **First player** runs `python3 main.py` - becomes the server
2. **Second player** (on same network) updates `HOST` in `main.py` to first player's IP address
3. **Second player** runs `python3 main.py` - connects as client

---

## 🧠 How the AI Works

The AI uses the **Minimax algorithm**, a classic recursive game theory approach that evaluates all possible future game states to select the optimal move.

### Algorithm Overview

```
Minimax Evaluation:
  +1  →  AI victory
  -1  →  Human victory
   0  →  Draw
```

**Key Concepts:**
- **Maximizing Player (AI)**: Tries to maximize the score (+1)
- **Minimizing Player (Human)**: Tries to minimize the score (-1)
- **Complete Search**: Evaluates all possible move sequences
- **Optimal Play**: Always selects the move leading to the best outcome

By recursively simulating all possible game states, the AI makes perfect decisions, making it **impossible to beat** (you can only draw or lose).

### Implementation Highlights

- Efficient board cloning for state exploration
- Depth-first recursive search
- Immediate evaluation of terminal states (win/loss/draw)
- Clean separation between AI logic and game engine

---

## 🎯 Usage Examples

### Starting a Server (PvP Mode)
```bash
$ python3 main.py
# Select option 1 for Player vs Player
Odaberi način igre:
1 — PvP (dva igrača preko mreže)
2 — PvAI (jedan igrač protiv računala)
Unos (1/2): 1
```

### Starting a Server (PvAI Mode)
```bash
$ python3 main.py
# Select option 2 for Player vs AI
Odaberi način igre:
1 — PvP (dva igrača preko mreže)
2 — PvAI (jedan igrač protiv računala)
Unos (1/2): 2
```

---

## 🏗️ Architecture & Design

### Design Principles

- **Separation of Concerns**: Game logic, AI, and UI are in separate modules
- **Modularity**: Each component can be used independently
- **Extensibility**: Easy to add new features or game modes
- **Clean Code**: Well-documented, readable, and maintainable

### Network Protocol

The application uses a simple JSON-based protocol over TCP sockets:

- **Messages**: `role`, `state`, `your_turn`, `move`, `error`
- **Data Format**: JSON objects with newline delimiters
- **Transport**: TCP/IP sockets (default port: 5000)

---

## 🛠️ Development

### Code Style

- Python 3 standard library conventions
- Clear variable naming
- Type hints in function signatures
- Comprehensive docstrings


---

## 👨‍💻 Authors

**Dominik Pavlisko**
**Matija Aleksić**

---

## 🙏 Acknowledgments

- Minimax algorithm implementation inspired by classic game theory
- Built as an educational project demonstrating AI and network programming concepts

---

**Enjoy the game! 🎲**
