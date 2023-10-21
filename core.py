class Place:
    #types: 0 = Caminho, 1 = Parede, S = Inicio, # = Fim
    def __init__(self, type, positionX, positionY, F = 0, G = 0, H = 0):
        self.type = type
        self.F = F
        self.G = G
        self.H = H
        self.positionX = positionX
        self.positionY = positionY

    def __str__(self):
        return self.type

class Board:
    def __init__(self):
        self.places = []
        self.start = None
        self.end = None

    def view_board(self):
        for line in self.places:
            for char in line:
                print(char.type, end=",")
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
                        elif char == "#":
                            self.end = place

                    count_rows += 1
                count_lines += 1
            self.calculate_variables()

    def calculate_variables(self):
        for line in self.places:
            for place in line: 
                if place.type == "0":
                    #calculate G
                    if place.positionX != self.start.positionX and place.positionY != self.start.positionY:
                        #diagonal
                        place.G = 14
                    else:
                        #verdical
                        place.G = 10

                    #calculate H
                    dx = abs(place.positionX - self.end.positionX)
                    dy = abs(place.positionY - self.end.positionY)
                    place.H = 10 * (dx + dy)

                    #calulate F
                    place.F = place.G + place.H

    def resolve(self):
        

b = Board()
b.create_using_file()
b.view_board()