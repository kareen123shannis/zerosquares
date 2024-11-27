import tkinter as tk
from tkinter import messagebox
import queue  

class State:
    def __init__(self, initial_board):
        self.board = [row[:] for row in initial_board]
        self.red_reached = False
        self.blue_reached = False

    def is_solved(self):
        return self.red_reached and self.blue_reached

    def move_square(self, r, c, dir):
        new_state = State(self.board)  
        new_r, new_c = r, c
        if dir == "Right":
            new_c = self.move_right(r, c, new_state)
        elif dir == "Left":
            new_c = self.move_left(r, c, new_state)
        elif dir == "Up":
            new_r = self.move_up(r, c, new_state)
        elif dir == "Down":
            new_r = self.move_down(r, c, new_state)

        if (new_r, new_c) != (r, c):
            new_state.board[new_r][new_c] = self.board[r][c]
            new_state.board[r][c] = 0

        return new_state 

    def move_right(self, r, c, new_state):
        while c < 10 and new_state.board[r][c + 1] == 0:
            c += 1
        return c

    def move_left(self, r, c, new_state):
        while c > 0 and new_state.board[r][c - 1] == 0:
            c -= 1
        return c

    def move_up(self, r, c, new_state):
        while r > 0 and new_state.board[r - 1][c] == 0:
            r -= 1
        return r

    def move_down(self, r, c, new_state):
        while r < 7 and new_state.board[r + 1][c] == 0:
            r += 1
        return r

    def square_reached(self, r, c):
        if self.board[r][c] == 1 and (r, c) == (5, 8):
            self.red_reached = True
            return True
        elif self.board[r][c] == 2 and (r, c) == (2, 7):
            self.blue_reached = True
            return True
        return False

    def next_state(self, dir):
        new_state = State(self.board)  
        for r in range(8):
            for c in range(11):
                if new_state.board[r][c] in [1, 2] and not new_state.square_reached(r, c):
                    new_state = new_state.move_square(r, c, dir)  
        for r in range(8):
            for c in range(11):
                new_state.square_reached(r, c)
        return new_state  

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.board))


    def __lt__(self, other):
        return False  

    def get_move_path(self):
        return []


class ZeroSquares:
    def __init__(self, master):
        self.master = master
        self.state = State([
            [0, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0],
            [-1, -1, 2, 0, 0, -1, -1, -1, -1, -1, 0],
            [-1, 0, 0, 0, 0, -1, -1, 0, 0, -1, 0],
            [-1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1],
            [-1, 0, 0, 0, -1, -1, -1, 0, 0, 0, -1],
            [-1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1],
            [-1, -1, 1, 0, -1, -1, -1, -1, -1, -1, 0],
            [0, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0]
        ])
        self.canvas = tk.Canvas(master, width=1800, height=400)
        self.canvas.pack()
        self.cell_size = 50
        self.draw_board()
        self.master.bind("<KeyPress>", self.on_key_press)

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(8):
            for c in range(11):
                self.draw_cell(r, c)

        self.square_borders(2, 7, 'blue')
        self.square_borders(5, 8, 'red')
        self.show_possible_moves()

    def draw_cell(self, r, c):
        x0 = c * self.cell_size
        y0 = r * self.cell_size
        x1 = x0 + self.cell_size
        y1 = y0 + self.cell_size
        color = self.get_color(self.state.board[r][c])
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline=color)

    def get_color(self, value):
        return {
            -1: 'black',
            1: 'red',
            2: 'blue',
            0: 'white'
        }.get(value, 'white')

    def square_borders(self, row, col, color):
        x0 = col * self.cell_size
        y0 = row * self.cell_size
        x1 = x0 + self.cell_size
        y1 = y0 + self.cell_size
        self.canvas.create_rectangle(x0, y0, x1, y1, outline=color, width=3)

    def show_possible_moves(self):
        possible_states = [
            self.state.next_state("Right"),
            self.state.next_state("Left"),
            self.state.next_state("Up"),
            self.state.next_state("Down")
        ]
        self.draw_possible_states(possible_states)

    def draw_possible_states(self, states):
        offset_x = 600
        for i, state in enumerate(states):
            for r in range(8):
                for c in range(11):
                    x0 = c * self.cell_size + (i * 180) + offset_x
                    y0 = r * self.cell_size
                    x1 = x0 + self.cell_size
                    y1 = y0 + self.cell_size
                    color = self.get_color(state.board[r][c])
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline=color)
            self.canvas.create_line(offset_x + (i * 220), 400, offset_x + (i * 220), 400, fill="black", width=2)

    def on_key_press(self, event):
        if not self.state.is_solved():
            dir = event.keysym
            self.state = self.state.next_state(dir)
            self.draw_board()
            if self.state.is_solved():
                messagebox.showinfo('Congrats', 'You won!')

    def bfs_search(self):
        initial_state = self.state
        queue = [(initial_state, [])]
        visited = set()
        visited.add(self.state)

        while queue:
            current_state, path = queue.pop(0)

            if current_state.is_solved():
                self.state = current_state
                print("BFS Path:", path)
                print("Visited:" ,len(visited))
                self.play_solution(path)
                return

            for dir in ["Right", "Left", "Up", "Down"]:
                next_state = current_state.next_state(dir)
                if next_state not in visited:
                    visited.add(next_state)
                    queue.append((next_state, path + [dir]))

        messagebox.showinfo('No solution', 'No solution found')

    def dfs_search(self):
      def dfs_recursive(current_state, path, visited):
        if current_state.is_solved():
            self.state = current_state
            print("DFS Path:", path)
            print("Visited:", len(visited))
            self.play_solution(path)  
            return True
        visited.add(current_state)

        for dir in ["Right", "Left", "Up", "Down"]:
            next_state = current_state.next_state(dir)

            if next_state not in visited:
                if dfs_recursive(next_state, path + [dir], visited):
                    return True

        return False

      visited = set()
      if not dfs_recursive(self.state, [], visited):
        messagebox.showinfo('No solution', 'No solution found')


    # def dfs_search(self):
    #     initial_state = self.state
    #     stack = [(initial_state, [])]
    #     visited = set()
    #     visited.add(self.state)

    #     while stack:
    #         current_state, path = stack.pop()

    #         if current_state.is_solved():
    #             self.state = current_state
    #             print("DFS Path:", path)
    #             print("Visited:" ,len(visited))
    #             self.play_solution(path)
    #             return

    #         for dir in ["Right", "Left", "Up", "Down"]:
    #             next_state = current_state.next_state(dir)
    #             if next_state not in visited:
    #                 visited.add(next_state)
    #                 stack.append((next_state, path + [dir]))

    #     messagebox.showinfo('No solution', 'No solution found')

    def ucs_search(self):
        initial_state = self.state
        pq = queue.PriorityQueue()  
        pq.put((0, initial_state, []))  
        visited = set()
        visited.add(initial_state)

        while not pq.empty():
            cost, current_state, path = pq.get()

            if current_state.is_solved():
                self.state = current_state
                print("UCS Path:", path)
                print("Visited:" ,len(visited))
                self.play_solution(path)
                return

            for dir in ["Right", "Left", "Up", "Down"]:
                next_state = current_state.next_state(dir)
                if next_state not in visited:
                    visited.add(next_state)
                    pq.put((cost + 1, next_state, path + [dir]))  

        messagebox.showinfo('No solution', 'No solution found')

    def play_solution(self, path):
      def execute_move(index):
        if index < len(path):
            move = path[index]
            self.state = self.state.next_state(move)  
            self.draw_board() 
            self.master.update()  
            self.master.after(500, execute_move, index + 1)  
        else:
            if self.state.is_solved():
                messagebox.showinfo('Congrats', 'You won!')  

      execute_move(0)

 


root = tk.Tk()
root.title("Zero Squares Game")
app = ZeroSquares(root)
root.after(1000, app.ucs_search)
root.mainloop()