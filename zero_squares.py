import tkinter as tk
from tkinter import messagebox
import queue

class State:
    def __init__(self, initial_board):
        self.board = [row[:] for row in initial_board]
        self.red_reached = False
        self.blue_reached = False
        self.cost = 0 

    def is_solved(self):
        return self.red_reached and self.blue_reached


    def __lt__(self, other):
        return self.cost < other.cost  

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
    def heuristic_sub(self, state):
     distance = 0
     for r in range(8):
        for c in range(11):
            if state.board[r][c] == 1:
                distance += abs(r - 5) + abs(c - 8) 
            elif state.board[r][c] == 2:
                distance += abs(r - 2) + abs(c - 7)  
     return distance 

    def next_state(self, dir):
     new_state = State(self.board)
    
     for r in range(8):
        for c in range(11):
            if new_state.board[r][c] in [1, 2] and not new_state.square_reached(r, c):
                new_state = new_state.move_square(r, c, dir)
    

     heuristic_score = self.heuristic_sub(new_state) 
     print(f"Heuristic Score: {heuristic_score}") 
     return new_state


    def eq(self, other):
        return self.board == other.board

    def hash(self):
        return hash(tuple(tuple(row) for row in self.board))

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
            [0, -1, -1, -1, -1, 0, 0, 0, 0 ,0 ,0]
        ])
        self.canvas = tk.Canvas(master, width=1800, height=400)
        self.canvas.pack()
        self.cell_size = 50
        self.draw_board()

        master.bind("<Right>", self.move_right)
        master.bind("<Left>", self.move_left)
        master.bind("<Up>", self.move_up)
        master.bind("<Down>", self.move_down)

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(8):
            for c in range(11):
                self.draw_cell(r, c)

        if not self.state.red_reached:
            self.square_borders(5 ,8,'red')

        if not self.state.blue_reached:
            self.square_borders(2 ,7,'blue')

        if self.state.is_solved():
            messagebox.showinfo("Congratulations!", "You have won the game!")
            self.master.quit()  

    def draw_cell(self, r, c):
        x0 = c * self.cell_size
        y0 = r * self.cell_size
        x1 = x0 + self.cell_size
        y1 = y0 + self.cell_size
        color = self.get_color(self.state.board[r][c])
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline=color)

    def get_color(self, value):
        if value == -1:
            return 'black'
        elif value == 1:  
            return 'red' if not self.state.red_reached else 'white'
        elif value == 2:  
            return 'blue' if not self.state.blue_reached else 'white'
        else:
            return 'white'

    def square_borders(self, r, c, color):
        x0 = c * self.cell_size
        y0 = r * self.cell_size
        x1 = x0 + self.cell_size
        y1 = y0 + self.cell_size
        self.canvas.create_rectangle(x0, y0, x1, y1, outline=color, width=3)

    def move_right(self, event):
        self.state = self.state.next_state("Right")
        self.draw_board()

    def move_left(self, event):
        self.state = self.state.next_state("Left")
        self.draw_board()

    def move_up(self, event):
        self.state = self.state.next_state("Up")
        self.draw_board()

    def move_down(self, event):
        self.state = self.state.next_state("Down")
        self.draw_board()

    def bfs_search(self):
        initial_state = self.state
        queue = [(initial_state, [])]
        visited = set()

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
        initial_state = self.state
        stack = [(initial_state, [])]
        visited = set()
        visited.add(self.state)

        while stack:
            current_state, path = stack.pop()

            if current_state.is_solved():
                self.state = current_state
                print("DFS Path:", path)
                self.play_solution(path)
                return

            for dir in ["Right", "Left", "Up", "Down"]:
                next_state = current_state.next_state(dir)
                if next_state not in visited:
                    visited.add(next_state)
                    stack.append((next_state, path + [dir]))

        messagebox.showinfo('No solution', 'No solution found')

    def dfs_recursive_search(self):
        def dfs_recursive(current_state, path):
            if current_state.is_solved():
                self.state = current_state
                print("DFS Path:", path)
                self.play_solution(path)  
                return True

            visited.add(current_state)

            for dir in ["Right", "Left", "Up", "Down"]:
                next_state = current_state.next_state(dir)

                if next_state not in visited:
                    if dfs_recursive(next_state, path + [dir]):
                        return True

            return False


        visited = set()
        if not dfs_recursive(self.state , []):
            messagebox.showinfo('No solution', 'No solution found')

    def ucs_search(self):
        initial_state = self.state
        pq = queue.PriorityQueue()  
        pq.put((0, initial_state, []))  
        
        visited = set()
        
        while not pq.empty():
            cost, current_state, path = pq.get()

            if current_state.is_solved():
                self.state = current_state
                print("UCS Path:", path)
                self.play_solution(path)
                return

            for dir in ["Right", "Left", "Up", "Down"]:
                next_state = current_state.next_state(dir)
                if next_state not in visited:
                    visited.add(next_state)
                    next_state.cost = cost + 1  
                    pq.put((next_state.cost, next_state, path + [dir])) 

        messagebox.showinfo('No solution', 'No solution found')

   

    def play_solution(self, path):
        for move in path:
            self.move_right("") if move == "Right" else \
            self.move_left("") if move == "Left" else \
            self.move_up("") if move == "Up" else \
            self.move_down("")

root = tk.Tk()
root.title("Zero Squares Game")
app = ZeroSquares(root)
# root.after(1000, app.ucs_search)
root.mainloop()