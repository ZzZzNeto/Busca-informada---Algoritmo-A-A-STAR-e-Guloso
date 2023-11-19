from meuamigofez import Place, Board
import time, os

class Board_WP(Board):
    def show_board(self):
        for line in self.places:
            for char in line:
                print(char.type, end=",")
            print("\n")

    def heuristic_WP(self, place, wolf):
        if wolf:
            return abs(place.positionX - self.end.positionX) + abs(place.positionY - self.end.positionY)
        else:
            return abs(place.positionX - self.start.positionX) + abs(place.positionY - self.start.positionY)

    def multiple_adjacents(self, place):
        adjacents = []
        for line in self.places:
            for char in line: 
                if char.positionX >= place.positionX - 1 and char.positionX <= place.positionX + 1 and char.positionY >= place.positionY - 1 and char.positionY <= place.positionY + 1:
                    if place.type == "W" and char.type == "P":
                        return ":)"
                    adjacents.append(char)
        
        return adjacents

    def create_for_WP(self):
        with open('template_WP.txt') as txt:
            count_lines = 0
            for line in txt:
                self.places.append([])
                count_rows = 0
                for char in line:
                    if char != "\n":
                        place = Place(char, count_rows, count_lines)
                        self.places[count_lines].append(place)

                        if char == "W":
                            self.start = place
                        elif char == "P":
                            self.end = place

                    count_rows += 1
                count_lines += 1

    def resolve_WP(self, moviment_wolf = 2, moviment_prey = 1):
        while True:
            adjacents_wolf = self.multiple_adjacents(self.start)
            adjacents_prey = self.multiple_adjacents(self.end)

            if adjacents_wolf == ":)":
                print("PEGO")
                break
            os.system('cls')
            
            for index in range(moviment_prey):
                run = None
                for adjacent in adjacents_prey:
                    if not adjacent.type == "P":
                        if adjacent.positionX != self.start.positionX and adjacent.positionY != self.start.positionY:
                            #diagonal
                            adjacent.g = self.end.g + 14
                        else:
                            #vertical
                            adjacent.g = self.end.g + 10
                        adjacent.h = self.heuristic_WP(adjacent, wolf=False)
                        adjacent.f = adjacent.g + adjacent.h

                        if not run:
                            run = adjacent
                        else:
                            if adjacent.f > run.f:
                                run = adjacent
                self.end.type = "0"
                self.end = run  
                self.end.type = "P" 
            
            for index in range(moviment_wolf):
                go = None
                for adjacent in adjacents_wolf:
                    if not adjacent.type == "W" and not adjacent.type == "1":
                        if adjacent.positionX != self.start.positionX and adjacent.positionY != self.start.positionY:
                            #diagonal
                            adjacent.g = self.start.g + 14
                        else:
                            #vertical
                            adjacent.g = self.start.g + 10
                        adjacent.h = self.heuristic_WP(adjacent, wolf=True)
                        adjacent.f = adjacent.g + adjacent.h
                        if not go:
                            go = adjacent
                        else:
                            if adjacent.h < go.h:
                                go = adjacent
                self.start.type = "0" 
                self.start = go  
                self.start.type = "W" 

            self.show_board()
            time.sleep(1)

b = Board_WP()
b.create_for_WP()
b.resolve_WP()