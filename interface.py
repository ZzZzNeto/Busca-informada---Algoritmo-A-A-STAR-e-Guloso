from tkinter import *
from core import Board
import time
class Maze:
    def __init__(self, master, rows, columns):
        self.master = master
        self.master.title('A Star')

        self.player_coords = {
            'column': None,
            'row': None,
        }

        self.exit_coords = {
            'column': None,
            'row': None,
        }

        self.rows = rows
        self.columns = columns
        self.maze = [["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                     ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                     ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                     ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                     ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                     ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                     ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                     ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                     ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                     ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                     ]
        self.count = 0
        self.buttons = [[None for _ in range(columns)] for _ in range(rows)]

        self.step_button = Button(
            self.master, text="Crie suas barreiras.", command=self.next_color_step)
        self.step_button.grid(row=rows + 1, columnspan=columns)

        self.text_area = Text(self.master, height=2)
        self.text_area.grid(row=rows, columnspan=columns, sticky="nsew")

        self.color_sequence = ["red", "blue", "green"]
        self.current_color_step = 0

    def run_interface(self):
        self.canvas = Canvas(self.master)

        self.master.geometry(f"{800}x{800}")
        for row in range(self.rows):
            for col in range(self.columns):
                button = Button(self.master, relief="ridge")
                button.grid(row=row, column=col, sticky="nsew")
                self.buttons[row][col] = button

                button["command"] = lambda r=row, c=col: self.change_color(
                    r, c)

        for i in range(self.rows):
            self.master.grid_rowconfigure(i, weight=1)
        for i in range(self.columns):
            self.master.grid_columnconfigure(i, weight=1)

    def change_color(self, row, col):
        button = self.buttons[row][col]

        if self.current_color_step == 1 and not self.player_coords['column']:
            self.player_coords = {
                'column': col,
                'row': row,
            }
        elif self.current_color_step == 1 and self.player_coords['column']:
            button1 = self.buttons[self.player_coords['row']
                                   ][self.player_coords['column']]
            button1.configure(background="SystemButtonFace")

            self.player_coords = {
                'column': col,
                'row': row,
            }

            self.text_area.insert(INSERT, '(!) Já existe um jogador\n')

            self.master.after(2000, self.remove_message)
        elif self.current_color_step == 2 and not self.exit_coords['column']:
            self.exit_coords = {
                'column': col,
                'row': row,
            }
        elif self.current_color_step == 2 and self.exit_coords['column']:
            button1 = self.buttons[self.exit_coords['row']
                                   ][self.exit_coords['column']]
            button1.configure(background="SystemButtonFace")

            self.exit_coords = {
                'column': col,
                'row': row,
            }
            self.text_area.insert(INSERT, '(!) Já existe uma saída\n')

            self.master.after(2000, self.remove_message)

        new_color = self.color_sequence[self.current_color_step]

        button.configure(background=new_color)

    def remove_message(self):
        self.text_area.delete(1.0, END)

    def next_color_step(self):
        self.current_color_step = self.current_color_step + 1

        if (self.current_color_step == 1):
            self.step_button.configure(
                text="Crie seu jogador.")
        elif (self.current_color_step == 2):
            self.step_button.configure(
                text="Crie a saída.")
        else:
            
            self.step_button = Button(
                self.master, text="Criar labirinto.", command=self.create_maze)
            self.step_button.grid(
                row=self.rows + 1, columnspan=self.columns, sticky="nsew")

    def create_maze(self):
        for row in range(self.rows):
            for col in range(self.columns):
                buttonColor = self.buttons[row][col]
                current_color = buttonColor.cget("background")

                if (current_color == 'red'):
                    self.maze[row][col] = "1"
                elif (current_color == 'green'):
                    self.maze[row][col] = "#"
                elif (current_color == 'blue'):
                    self.maze[row][col] = "S"

        self.create_file()
        
       

    def create_file(self):
        with open("template.txt", "w") as file:
            for line in self.maze:
                for char in line:
                    file.write(char)
                file.write("\n")
        
        self.step_button = Button(
                self.master, text="Resolver labirinto", command=self.resolve_maze)
        self.step_button.grid(
            row=self.rows + 1, columnspan=self.columns, sticky="nsew")
    
        
    def resolve_maze(self):
        b = Board()
        b.create_using_file()
        b.view_board()
        b.resolve(self)
    def move_player(self, row, col):
        
        buttonNewPlace = self.buttons[col][row]
        if self.count == 0:
            buttonOldPlace = self.buttons[self.player_coords['row']][self.player_coords['column']]
            self.count+=1
        else:
            buttonOldPlace = self.buttons[self.player_coords['column']][self.player_coords['row']]

        
        self.player_coords = {
            'column': col,
            'row': row,
        }
        buttonNewPlace.configure(background="blue")
        buttonOldPlace.configure(background="SystemButtonFace")
        
        self.master.update()        
        time.sleep(0.2)
        
root = Tk()
maze = Maze(root, 10, 10)
maze.run_interface()
root.mainloop()