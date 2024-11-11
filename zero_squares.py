import tkinter as tk
from tkinter import messagebox


class State:
    def __init__(self, initial_board):
        self.board = [row[:] for row in initial_board]
        self.red_reached = False
        self.blue_reached = False

    def is_solved(self):
        return self.red_reached and self.blue_reached

    def move_square(self, r, c, dir):
        new_r, new_c = r, c
        if dir == "Right":
            new_c = self.move_right(r, c)
        elif dir == "Left":
            new_c = self.move_left(r, c)
        elif dir == "Up":
            new_r = self.move_up(r, c)
        elif dir == "Down":
            new_r = self.move_down(r, c)

        if (new_r, new_c) != (r, c):
            self.board[new_r][new_c] = self.board[r][c]
            self.board[r][c] = 0

    def move_right(self, r, c):
        while c < 10 and self.board[r][c + 1] == 0:
            c += 1
        return c

    def move_left(self, r, c):
        while c > 0 and self.board[r][c - 1] == 0:
            c -= 1
        return c

    def move_up(self, r, c):
        while r > 0 and self.board[r - 1][c] == 0:
            r -= 1
        return r

    def move_down(self, r, c):
        while r < 7 and self.board[r + 1][c] == 0:
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
                    new_state.move_square(r, c, dir)
        return new_state




















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






if __name__ == "__main__":
    root = tk.Tk()
    app = ZeroSquares(root)
    root.mainloop()
