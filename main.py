import json
import socket
import threading
import tkinter as tk
from tkinter import messagebox

from GameEngine import GameEngine
from AIEngine import AIEngine

HOST = "127.0.0.1"
PORT = 5000


def send_json(conn, data: dict):
    text = json.dumps(data) + "\n"
    conn.sendall(text.encode("utf-8"))


def recv_line(conn):
    buffer = b""
    while True:
        chunk = conn.recv(1)
        if not chunk:
            return None
        if chunk == b"\n":
            break
        buffer += chunk
    return buffer.decode("utf-8")


def try_connect_once(host, port, timeout=0.5):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((host, port))
        s.settimeout(None)
        return s
    except OSError:
        s.close()
        return None


def run_server(host, port, ai_enabled=False):
    """
    PvP: čeka 2 klijenta (X i O)
    PvAI: čeka 1 klijenta (X), AI igra kao O
    """
    engine = GameEngine()
    ai = AIEngine() if ai_enabled else None

    if ai_enabled:
        print("[SERVER] PvAI (čovjek = X, AI = O).")
    else:
        print("[SERVER] PvP (X i O su ljudi).")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(2)
        print(f"[SERVER] Čekam igrače na {host}:{port}...")

        # X se spaja prvi
        conn_x, addr_x = s.accept()
        print(f"[SERVER] Spojio se X: {addr_x}")
        send_json(conn_x, {"type": "role", "mark": "X"})

        conn_o = None
        if ai_enabled:
            print("[SERVER] Koristim AI kao igrača O.")
        else:
            conn_o, addr_o = s.accept()
            print(f"[SERVER] Spojio se O: {addr_o}")
            send_json(conn_o, {"type": "role", "mark": "O"})

        players = {"X": conn_x, "O": conn_o}

        def broadcast_state(extra=None):
            state = {
                "type": "state",
                "board": engine.board,
                "current_player": engine.current_player,
            }
            if extra:
                state.update(extra)

            try:
                send_json(conn_x, state)
            except OSError:
                pass

            if conn_o:
                try:
                    send_json(conn_o, state)
                except OSError:
                    pass
        broadcast_state()

        while True:
            current = engine.current_player

            if current == "X" or (current == "O" and not ai_enabled):
                conn = players[current]
                if conn is None:
                    print("[SERVER] Očekivana konekcija nije dostupna. Kraj servera.")
                    break

                try:
                    send_json(conn, {"type": "your_turn"})
                except OSError:
                    print("[SERVER] Ne mogu poslati 'your_turn' — veza prekinuta.")
                    break

                line = recv_line(conn)
                if line is None:
                    print("[SERVER] Igrač se odspojio. Kraj servera.")
                    break

                try:
                    msg = json.loads(line)
                except json.JSONDecodeError:
                    print("[SERVER] Neispravan JSON.")
                    continue

                if msg.get("type") != "move":
                    print("[SERVER] Očekivan 'move'.")
                    continue

                row = msg.get("row")
                col = msg.get("col")
                if row is None or col is None:
                    continue

                try:
                    result = engine.play_move(int(row), int(col))
                except Exception as e:
                    print(f"[SERVER] Greška pri play_move: {e}")
                    try:
                        send_json(conn, {"type": "error", "message": "Server error."})
                    except Exception:
                        pass
                    continue

                if not result["valid"]:
                    try:
                        send_json(conn, {"type": "error", "message": "Polje je već zauzeto."})
                    except Exception:
                        pass
                    continue

            else:
                try:
                    best = ai.get_best_move(engine)
                except Exception as e:
                    print(f"[SERVER] AI iznimka: {e}")
                    break

                if best is None:
                    print("[SERVER] AI nema poteza.")
                    break

                row, col = best
                print(f"[SERVER] AI odigrao: ({row}, {col})")
                result = engine.play_move(row, col)

            extra = {"winner": result["winner"], "draw": result["draw"]}
            broadcast_state(extra)

            if result["winner"] or result["draw"]:
                print("[SERVER] Igra gotova.")
                break

        try:
            conn_x.close()
        except Exception:
            pass
        if conn_o:
            try:
                conn_o.close()
            except Exception:
                pass

        print("[SERVER] Server završio.")


class TicTacToeNetworkGUI:
    def __init__(self, sock: socket.socket):
        self.sock = sock
        self.listener_thread = None

        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe LAN")

        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        self.my_mark = None
        self.current_player = None
        self.is_my_turn = False

        self.status_label = tk.Label(self.root, text="Spajanje...", font=("Arial", 14))
        self.status_label.grid(row=0, column=0, columnspan=3, pady=(10, 10))

        self._create_board()

        self.exit_btn = tk.Button(self.root, text="Izađi", font=("Arial", 12), command=self.on_close)
        self.exit_btn.grid(row=4, column=0, columnspan=3, pady=(10, 10))

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.disable_board()

        self.listener_thread = threading.Thread(target=self.listen_loop, daemon=True)
        self.listener_thread.start()

    def _create_board(self):
        for r in range(3):
            for c in range(3):
                btn = tk.Button(
                    self.root,
                    text="",
                    width=6,
                    height=3,
                    font=("Arial", 20),
                    command=lambda row=r, col=c: self.on_cell_click(row, col),
                )
                btn.grid(row=r + 1, column=c, padx=5, pady=5)
                self.buttons[r][c] = btn

    def listen_loop(self):
        try:
            while True:
                line = recv_line(self.sock)
                if line is None:
                    self.root.after(0, self.handle_server_disconnect)
                    break

                try:
                    msg = json.loads(line)
                except json.JSONDecodeError:
                    continue

                self.root.after(0, self.handle_message, msg)
        except OSError:
            pass

    def handle_server_disconnect(self):
        messagebox.showinfo("Veza prekinuta", "Veza sa serverom je prekinuta.")
        self.disable_board()
        self.status_label.config(text="Veza prekinuta.")

    def handle_message(self, msg: dict):
        mtype = msg.get("type")

        if mtype == "role":
            self.my_mark = msg.get("mark")
            self.root.title(f"Tic-Tac-Toe LAN – Igrač {self.my_mark}")
            self.status_label.config(text=f"Ti si igrač {self.my_mark}. Čekam početak igre...")

        elif mtype == "state":
            self.board = msg.get("board", self.board)
            self.current_player = msg.get("current_player", self.current_player)
            winner = msg.get("winner")
            draw = msg.get("draw")

            self.update_board_view()

            if winner:
                self.status_label.config(text=f"Pobijedio je {winner}")
                messagebox.showinfo("Kraj igre", f"Pobijedio je {winner}")
                self.disable_board()
                self.is_my_turn = False
            elif draw:
                self.status_label.config(text="Neriješeno")
                messagebox.showinfo("Kraj igre", "Neriješeno!")
                self.disable_board()
                self.is_my_turn = False
            else:
                self.status_label.config(text=f"Igrač na potezu: {self.current_player}")

        elif mtype == "your_turn":
            self.is_my_turn = True
            self.enable_board()
            if self.my_mark:
                self.status_label.config(text=f"Tvoj potez ({self.my_mark})")
            else:
                self.status_label.config(text="Tvoj potez")

        elif mtype == "error":
            err_msg = msg.get("message", "Nepoznata greška.")
            messagebox.showwarning("Greška", err_msg)

    def update_board_view(self):
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(text=self.board[r][c])

    def disable_board(self):
        for row in self.buttons:
            for btn in row:
                btn.config(state=tk.DISABLED)

    def enable_board(self):
        for row in self.buttons:
            for btn in row:
                btn.config(state=tk.NORMAL)

    def on_cell_click(self, row: int, col: int):
        if not self.is_my_turn:
            return
        if self.board[row][col] != "":
            return

        move_msg = {"type": "move", "row": row, "col": col}
        try:
            self.sock.sendall((json.dumps(move_msg) + "\n").encode("utf-8"))
        except OSError:
            messagebox.showerror("Greška", "Veza sa serverom je prekinuta.")
            self.disable_board()
            self.is_my_turn = False
            return

        self.is_my_turn = False
        self.disable_board()

    def on_close(self):
        try:
            if self.sock:
                self.sock.close()
        except OSError:
            pass
        self.root.destroy()

    def run(self):
        self.root.mainloop()


def main():
    print("Odaberi način igre:")
    print("1 — PvP (2 igrača)")
    print("2 — PvAI")
    mode = input("Unos (1/2): ").strip()

    if mode == "1":
        print("PvP odabir:")
        print("1 — Host (pokreni server)")
        print("2 — Join (spoji se na server)")
        choice = input("Unos (1/2): ").strip()

        if choice == "1":
            # HOST
            host_bind = "0.0.0.0"
            print(f"[APP] Hostam igru na {host_bind}:{PORT}")
            print("➡️  Daj drugom igraču svoj LAN IP (npr. 192.168.1.50) i port:", PORT)

            server_thread = threading.Thread(
                target=run_server, args=(host_bind, PORT, False), daemon=True
            )
            server_thread.start()

            # Host se spaja kao klijent preko localhost
            sock = None
            while sock is None:
                sock = try_connect_once("127.0.0.1", PORT)

            print("[APP] Spojen kao HOST (X).")
            app = TicTacToeNetworkGUI(sock)
            app.run()
            return

        elif choice == "2":
            # JOIN
            ip = input("Unesi IP adresu hosta (npr. 192.168.1.50): ").strip()

            sock = try_connect_once(ip, PORT, timeout=3.0)
            if not sock:
                print("[APP] Ne mogu se spojiti. Provjeri IP/port i firewall.")
                return

            print("[APP] Spojen kao JOIN (O).")
            app = TicTacToeNetworkGUI(sock)
            app.run()
            return

        else:
            print("Neispravan odabir.")
            return

    else:
        print("[APP] Pokrećem PvAI...")
        server_thread = threading.Thread(
            target=run_server, args=("127.0.0.1", PORT, True), daemon=True
        )
        server_thread.start()

        sock = None
        while sock is None:
            sock = try_connect_once("127.0.0.1", PORT)

        app = TicTacToeNetworkGUI(sock)
        app.run()


if __name__ == "__main__":
    main()
