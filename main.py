import math, time
import os

class Place:
    #types: 0 = Caminho, 1 = Parede, S = Inicio, # = Fim, P = Player
    def __init__(self, type, positionX, positionY, F = 0, G = None, H = 0, C = None):
        self.type = type
        self.F = F
        self.C = C
        self.positionX = positionX
        self.positionY = positionY
        self.visited = False
        self.penultimate = None

    def __str__(self):
        return self.type
    
class Board:
    
    def __init__(self):
        self.places = []
        self.initialPosition = None
        self.start = None
        self.end = None
        self.rightWay = []
        
    def show_board(self):
        for line in self.places:
            for char in line:
                print(char.type, end=",")
            print("\n")

    def heuristic(self, place):
        #calculate G
        if place.positionX != self.start.positionX and place.positionY != self.start.positionY:
            #diagonal
            place.G = 14
        else:
            #vertical
            place.G = 10
        
        #calculate H
        constant = 10
        dx = abs(place.positionX - self.end.positionX)
        dy = abs(place.positionY - self.end.positionY)
        
        place.H = constant * (dx + dy)
        #calulate F
        place.F = place.G + place.H
    
    def create_board_using_file(self):
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
                            place.C = 0
                            self.initialPosition = place
                            self.start = place
                        elif char == "#":
                            self.end = place

                    count_rows += 1
                count_lines += 1
            
            # self.calculate_variables()
    
    def change_place(self, place, C):
        x_squared = (place.positionX - self.end.positionX) ** 2
        y_squared = (place.positionY - self.end.positionY) ** 2
        
        square_root = math.sqrt(x_squared + y_squared)

        place.C = C
        place.F = round(square_root + C, 2)

    def calculate_distance(self, current_place, accumulator = 1):

        x, y = current_place.positionX, current_place.positionY
        startPosition, endPosition = {"x": x - accumulator, "y": y - accumulator}, {"x": x + accumulator, "y": y + accumulator}
        hasChanges = False

        for row in self.places:
            for place in row:
                # Calcular linhas superiores ao centro
                if place.positionX == startPosition['x'] and (place.positionY >= startPosition['y'] and place.positionY <= endPosition['y']):
                    self.change_place(place, accumulator) 
                    hasChanges = True

                # Calcular linhas inferiores ao centro
                elif place.positionX == endPosition['x'] and (place.positionY >= startPosition['y'] and place.positionY <= endPosition['y']):
                    self.change_place(place, accumulator)
                    hasChanges = True

                # Calcular colunas da esquerda
                elif place.positionY == startPosition['y'] and (place.positionX >= startPosition['x'] and place.positionX <= endPosition['x']):
                    self.change_place(place, accumulator) 
                    hasChanges = True
                
                # Calcular colunas da direita
                elif place.positionY == endPosition['y'] and (place.positionX >= startPosition['x'] and place.positionX <= endPosition['x']):
                    self.change_place(place, accumulator) 
                    hasChanges = True

        if not hasChanges:
            return
        print(24*'-')
        return self.calculate_distance(current_place, accumulator + 1)
    
    def get_adjacents(self, place):
        adjacents = []
        for line in self.places:
            for char in line: 
                if char.positionX >= place.positionX - 1 and char.positionX <= place.positionX + 1 and char.positionY >= place.positionY - 1 and char.positionY <= place.positionY + 1 and char.type != 'S' and char.type != '-':
                    adjacents.append(char)
        
        return adjacents
    
    def get_adjacents_back(self, place):
        adjacents = []
        for line in self.places:
            for char in line: 
                if char.positionX >= place.positionX - 1 and char.positionX <= place.positionX + 1 and char.positionY >= place.positionY - 1 and char.positionY <= place.positionY + 1 and char.type != 'S' and char.type != '0':
                    adjacents.append(char)
        
        return adjacents
    
    def get_next_steps(self, place, steps = []):
        adjacents = self.get_adjacents(place)
        
        lowerStep = None
        for adjacent in adjacents:
            if adjacent.type != '1' and adjacent.type != '-':
                if lowerStep:
                    if adjacent.F <= lowerStep.F or adjacent.C >= lowerStep.C:
                        lowerStep = adjacent
                else:
                    lowerStep = adjacent
                    
        if not lowerStep or lowerStep.type == '#':
            # place.type = "-"
            # lowerStep.type = "S"
            # steps.append(lowerStep)

            return steps
        self.penultimate = lowerStep
        
        place.type = "-"
        lowerStep.type = "S"
        steps.append(lowerStep)

        # if lowerStep.type == '#':
        #     return steps
    
        return self.get_next_steps(lowerStep, steps)
    
    def define_best_way(self):
        steps = self.get_next_steps(self.start)
        steps.reverse()
        
        lowerStep = None
        for current_place in steps:
            if lowerStep and self.initialPosition.positionX == lowerStep.positionX and self.initialPosition.positionY == lowerStep.positionY:
                self.reset_board(steps)
                return

            adjacents = self.get_adjacents_back(lowerStep if lowerStep else current_place)
            for adjacent in adjacents:
                if adjacent.type == '-':
                    if lowerStep:
                        if adjacent.F < lowerStep.F and adjacent.C < lowerStep.C:
                            lowerStep = adjacent
                    else:
                        lowerStep = adjacent
            
            self.rightWay.append(lowerStep)

    def reset_board(self, steps):
        for step in steps:
            if step.type == '-':
                step.type = '0'
            elif step.type == 'S':
                step.type = '0'
    

    def resolve(self):
        reversedList = self.rightWay
        reversedList.reverse()
        for place in reversedList:
            place.type = "*"
            
            os.system("cls")
            self.show_board()
            time.sleep(1)
            
        self.penultimate.type = "*"
            
        os.system("cls")
        self.show_board()
        time.sleep(1)
    
b = Board()
b.create_board_using_file()
b.calculate_distance(b.start)
b.define_best_way()
b.resolve()