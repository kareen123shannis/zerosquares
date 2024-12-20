import tkinter as tk
from tkinter import messagebox
import queue
import copy

from matplotlib.pyplot import step 
class State:
    def __init__(self, initial_board):
        self.board = [row[:] for row in initial_board]
        self.red_reached = False
        self.blue_reached = False
        self.cost = 0  
        self.f = 0
        self.move_path = []

    def is_solved(self):
        return self.red_reached and self.blue_reached

    def __lt__(self, other):
        return self.f < other.f  

    def move_square(self, r, c, dir):
     new_state = copy.deepcopy(self)  
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

    def next(self):
     next_state = []
     current = copy.deepcopy(self)

     print("Generating neighbors...")


     for r in range(8):  
        for c in range(11): 
            if current.board[r][c] in [1, 2]:  
                new_c = current.move_right(r, c, current)  
                if new_c != c:  
                    next_state.append(current.move_square(r, c, "Right"))
                break  

     for r in range(8):
        for c in range(11):
            if current.board[r][c] in [1, 2]:
                new_c = current.move_left(r, c, current)
                if new_c != c:
                    next_state.append(current.move_square(r, c, "Left"))
                break


     for r in range(8):
        for c in range(11):
            if current.board[r][c] in [1, 2]:
                new_r = current.move_up(r, c, current)
                if new_r != r:
                    next_state.append(current.move_square(r, c, "Up"))
                break

    
     for r in range(8):
        for c in range(11):
            if current.board[r][c] in [1, 2]:
                new_r = current.move_down(r, c, current)
                if new_r != r:
                    next_state.append(current.move_square(r, c, "Down"))
                break

     return next_state


     

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
        if self.board[r][c] == 1 and r == 4 and c == 9:
            self.red_reached = True
            return True
        elif self.board[r][c] == 2 and r == 2 and c == 7:
            self.blue_reached = True
            return True
        return False
    def heuristic_sub(self):
     distance = 0
     for r in range(8):
        for c in range(11):
            if self.board[r][c] == 1:  
                distance += abs(r - 4) + abs(c - 9)  
            elif self.board[r][c] == 2:  
                distance += abs(r - 2) + abs(c - 7)  
     return distance


    def next_state(self, dir):
     new_state = copy.deepcopy(self)
     

     for r in range(8):
        for c in range(11):
            if new_state.board[r][c] in [1, 2] and not new_state.square_reached(r, c):
                new_state = new_state.move_square(r, c, dir)

     new_state.cost = self.cost + 1  
    
     heuristic_score = self.heuristic_sub()  
     new_state.f = new_state.cost + heuristic_score  


     new_state.move_path = self.move_path + [dir]
    
     return new_state

    def get_move_path(self):
        return self.move_path  

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
            [-1, -1, 1, 0, 0, -1, -1, -1, -1, -1, 0],
            [-1, 0, 0, 0, 0, -1, -1, 0, 0, -1, 0],
            [-1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1],
            [-1, 0, 0, 0, -1, -1, -1, 0, 0, 0, -1],
            [-1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1],
            [-1, -1, 2, 0, -1, -1, -1, -1, -1, -1, 0],
            [0, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0]
        ])
        self.canvas = tk.Canvas(master, width=1800, height=400)
        self.canvas.pack()
        self.cell_size = 50
        self.draw_board()
        self.game_solved = False
        self.solved_shown = False 
        self.move_label = tk.Label(master, text="Path: ", font=("Arial", 14))
        self.move_label.pack()

        master.bind("<Right>", self.move_right)
        master.bind("<Left>", self.move_left)
        master.bind("<Up>", self.move_up)
        master.bind("<Down>", self.move_down)
    
    def heuristic_sub(self, state):
        distance = 0
        for r in range(8):
            for c in range(11):
                if state.board[r][c] == 1:
                    distance += abs(r - 4) + abs(c - 9)
                elif state.board[r][c] == 2:
                    distance += abs(r - 2) + abs(c - 7)
        return distance
    def draw_board(self):
        self.canvas.delete("all")
        for r in range(8):
            for c in range(11):
                self.draw_cell(r, c)
        if not self.state.red_reached:
            self.square_borders(4 ,9,'red')
        if not self.state.blue_reached:
            self.square_borders(2 ,7,'blue')
        if self.state.is_solved():
            self.game_solved = True
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


    def a_star_search(self):
     initial_state = self.state
     pq = queue.PriorityQueue()  
     pq.put((0 + self.heuristic_sub(initial_state), 0, initial_state, []))  

     visited = set()

     while not pq.empty():
        _, cost, current_state, path = pq.get()

    
        if current_state.is_solved():
            self.state = current_state
            print(f"Path length: {len(path) }")
            print(f"visited len: {len(visited)}")  
            self.play_solution(path)
            return

        
        if current_state not in visited:
            visited.add(current_state)

    
        for dir in ["Right", "Left", "Up", "Down"]:
            next_state = current_state.next_state(dir)

        
            if next_state not in visited:
                visited.add(next_state)  
                next_cost = cost + 1
                heuristic = self.heuristic_sub(next_state)
                pq.put((next_cost + heuristic, next_cost, next_state, path + [dir]))

                
                
     messagebox.showinfo('No solution', 'No solution found')           
        
    
     
    def execute_move(self, next_state, path):
        self.state = next_state
        self.draw_board()
        if self.state.is_solved():
            messagebox.showinfo('Congrats', 'Solution completed!')

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
            print("Visited:", len(visited))
            self.play_solution(path)
            return

    
        for direction in ["Right", "Left", "Up", "Down"]:
            next_state = current_state.next_state(direction)

        
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path + [direction]))

                self.master.after(1000, self.execute_move, next_state, path + [direction])
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
                print("Dfs Path:",  current_state.get_move_path()) 
                print("Visited:" ,len(visited))
                self.play_solution(path)
                return
            for dir in ["Right", "Left", "Up", "Down"]:
                next_state = current_state.next_state(dir)
                if next_state not in visited:
                    visited.add(next_state)
                    stack.append((next_state, path + [dir]))
                    print(f"Step {len(path) + 1}/{len(path) + 1}: {dir}")
                    print(f"Path length: {len(path) + 1}")
        messagebox.showinfo('No solution', 'No solution found')

    
    def dfs_recursive_search(self):
        def dfs_recursive(current_state, path):
            if current_state.is_solved():
                self.state = current_state
                print("Dfs_recursive Path:",  current_state.get_move_path()) 
                print("Visited:" ,len(visited))
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
                print("Ucs Path:",  current_state.get_move_path())
                print("Visited:" ,len(visited)) 
                self.play_solution(path)
                return
            for dir in ["Right", "Left", "Up", "Down"]:
                next_state = current_state.next_state(dir)
                if next_state not in visited:
                    visited.add(next_state)
                    next_state.cost = cost + 1  
                    pq.put((next_state.cost, next_state, path + [dir])) 
                
        messagebox.showinfo('No solution', 'No solution found')

    def simple_hill_climbing(self):
     current_state = self.state
     visited = set()  
     print("Hill Climbing: Starting...")

     step = 0  
     prev_heuristic = self.heuristic_sub(current_state)

     while True:
    
        neighbors = current_state.next()  
        if not neighbors:
            print("Hill Climbing: No neighbors found.")
            break

    
        step += 1
        print(f"Step: {step}")
        print("Generating neighbors...")

        print("Evaluating neighbors...")

    
        next_state = None
        best_heuristic = float('inf')

        for neighbor in neighbors:
            
            heuristic_value = self.heuristic_sub(neighbor)
            print(f"Neighbor heuristic: {heuristic_value}")  

            if heuristic_value < best_heuristic:
                best_heuristic = heuristic_value
                next_state = neighbor

        if next_state is None:
            print("Hill Climbing: No improvement found.")
            break

        if best_heuristic < prev_heuristic:
            current_state = next_state
            self.state = current_state
            self.draw_board()  
            prev_heuristic = best_heuristic  
            print(f"Step: {step}")  
             
            if current_state.is_solved():
                print("Hill Climbing: Solution found!")
                print(f"Path to solution: {current_state.get_move_path()}")
                break
        else:
            print("Hill Climbing: No improvement found.")
            break

    def steepest_ascent_hill_climbing(self):
     current_state = self.state
     visited = set()  
     print("Steepest Ascent Hill Climbing: Starting...")

     step = 0
     prev_heuristic = self.heuristic_sub(current_state)

     while True:
        neighbors = current_state.next()  
        if not neighbors:
            print("Steepest Ascent Hill Climbing: No neighbors found.")
            break

        step += 1
        print(f"Step: {step}")
        print("Generating neighbors...")
        print("Evaluating neighbors...")

        next_state = None
        best_heuristic = float('inf')  

        for neighbor in neighbors:
            heuristic_value = self.heuristic_sub(neighbor)
        

    
            if heuristic_value < best_heuristic:
                best_heuristic = heuristic_value
                next_state = neighbor

        if next_state is None:
            print("Steepest Ascent Hill Climbing: No improvement found.")
            break

        
        if best_heuristic < prev_heuristic:
            current_state = next_state
            self.state = current_state
            self.draw_board()
            prev_heuristic = best_heuristic 
            print(f"Step: {step}")

            if current_state.is_solved():
                print("Steepest Ascent Hill Climbing: Solution found!")
                
                break
        else:
            print("Steepest Ascent Hill Climbing: No improvement found.")
            break
    def play_solution(self, path):
        for move in path:
            self.move_right("") if move == "Right" else \
            self.move_left("") if move == "Left" else \
            self.move_up("") if move == "Up" else \
            self.move_down("")

root = tk.Tk()
root.title("Zero Squares Game")
app = ZeroSquares(root)
root.after(1000, app.simple_hill_climbing)
root.mainloop()