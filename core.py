from Stack import Stacks
import os, time
from tkinter import *

class Player:
    def __init__(self, initialPosition):
        self.current_position = initialPosition
        self.initialPosition = initialPosition
        self.accumulator = 0
        
        self.top = None
        self.bottom = None
        self.right = None
        self.left = None
        self.top_left = None
        self.top_right = None
        self.bottom_left = None
        self.bottom_right = None
    
    def on_change_position(self, new_position):
        self.current_position = new_position

        x, y = new_position.positionX, new_position.positionY
        currentX, currentY = self.current_position.positionX, self.current_position.positionY

        if currentX != x and currentY != y:
            # Andou para as diagonais
            self.accumulator += 14
        else:
            # Andou para horizontal ou vertical
            self.accumulator += 10

        print('NOVO G', self.accumulator)

class Place:
    #types: 0 = Caminho, 1 = Parede, S = Inicio, # = Fim, P = Player
    def __init__(self, type, positionX, positionY, F = 0, G = 0, H = 0):
        self.type = type
        self.F = F
        self.G = G
        self.H = H
        self.positionX = positionX
        self.positionY = positionY
        self.valid = True

    def __str__(self):
        return self.type

class Board:
    def __init__(self):
        self.places = []
        self.start = None
        self.end = None
        self.player = None

    def view_board(self):
        for line in self.places:
            for char in line:
                print(char.H, end=",")
            print("\n")

    def create_using_interface(self):
        pass

    def create_using_file(self):
        with open('template.txt') as txt:
            count_lines = 0
            for line in txt:
                self.places.append([])
                count_rows = 0
                for char in line:
                    if char != "\n":
                        place = Place(char, count_rows, count_lines)
                        self.places[count_lines].append(place)

                        if char == "S":
                            self.start = place
                            self.player = Player(place)
                        elif char == "#":
                            self.end = place

                    count_rows += 1
                count_lines += 1
            self.calculate_variables()

    def calculate_variables(self):
        for line in self.places:
            for place in line: 
                if place.type == "0" or place.type == "#":
                    print(place)
                    #calculate G
                    if place.positionX != self.start.positionX and place.positionY != self.start.positionY:
                        #diagonal
                        place.G = 14
                    else:
                        #vertical
                        place.G = 10 
                    
                    #calculate H
                    dx = abs(place.positionX - self.end.positionX)
                    dy = abs(place.positionY - self.end.positionY)
                    place.H = 10 * (dx + dy)

                    #calulate F
                    place.F = place.G + place.H
    
    def get_adjacents(self, place):
        adjacents = []
        for line in self.places:
            for char in line: 
                if char.positionX >= place.positionX - 1 and char.positionX <= place.positionX + 1 and char.positionY >= place.positionY - 1 and char.positionY <= place.positionY + 1 and char.type != 'S' and char.type != '-':
                    adjacents.append(char)
        
        return adjacents

    def next_step(self, place, steps = Stacks(100)):
        adjacents = self.get_adjacents(place)
        
        # Identifica próximo passo. Por padrão, o valor é posição que fica no top_left. 
        lowerStep = None
        
        for adjacent in adjacents:
            if adjacent.valid and not adjacent.type == '1':
                if lowerStep:
                    if adjacent.F < lowerStep.F:
                        lowerStep = adjacent
                else:
                    lowerStep = adjacent
        
        # print('próxima etapa', {lowerStep.positionX, lowerStep.positionY})
        # Se não houver nenhum passo, o local dele não muda, então deve desempilhar
        if not lowerStep and steps.getRowLength() > 0:
            place.valid = False
            steps.unStack()
            print('entrou quando:', {place.positionX, place.positionY})
            place.type = "0"
            if steps.getTop():
                steps.getTop().type = "S"
            else: 
                print("Impossible!")
                return False

            return self.next_step(steps.getTop(), steps)
        
        steps.stackUp(lowerStep)

        # if not lowerStep or lowerStep.type == '#':
        #     for step in steps.getValues():
        #         if step:
        #             step.type = "0"
        #     node = steps.getTop()
        #     right_path = []
            
        #     start_adjacentes = self.get_adjacents(self.start)
        #     while node not in start_adjacentes: 
        #         node_adjacents = self.get_adjacents(node)
        #         minior = node_adjacents[0]
        #         for x in node_adjacents:
        #             if x.F < minior.F and x.F != 0:
        #                 print(x.F, minior.F)
        #                 minior = x
                
        #         right_path.append(node)
        #         node = minior

            
        #     return right_path
        
        place.type = "-"
        lowerStep.type = "S"
        self.player.on_change_position(place)
        place.G = self.player.current_position.G
        
        return self.next_step(lowerStep, steps)

    def resolve(self, maze):
        steps = self.next_step(self.start)
        
        if not steps.isEmpty(): 
            steps.showFullStack()
            for index in range(0, steps.getTopIndex()):
                allValues = steps.getValues()
                if allValues[index]:
                    currentStep = allValues[index]
                    currentStep.type = "S"
                    os.system("cls")
                    self.view_board()
                    maze.move_player(currentStep.positionX, currentStep.positionY)
                    time.sleep(1) 
                    currentStep.type = "-"
                    
b = Board()
b.create_using_file()
b.view_board()
b.resolve(b.places)