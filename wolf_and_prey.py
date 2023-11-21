from main import Place, Board
import time, os
import heapq

class Board_WP(Board):
    def show_board(self):
        for line in self.places:
            for char in line:
                print(char.type, end=",")
            print("\n")

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

    def multiple_adjacents(self, place):
        adjacents = []
        for line in self.places:
            for char in line: 
                if char.positionX >= place.positionX - 1 and char.positionX <= place.positionX + 1 and char.positionY >= place.positionY - 1 and char.positionY <= place.positionY + 1:
                    if place.type == "W" and char.type == "P":
                        return ":)"
                    adjacents.append(char)
        
        return adjacents

    def a_star_WP(self, start, goal, run = False):
        start.G = 0
        start.H = self.calculate_distance_manhattan(
            start, goal)
        start.F = start.H + start.G

        open_list = [(start.F, start)]
        closed_list = set()
        current = start

        while open_list:
            f, competitor = heapq.heappop(open_list)

            if competitor and competitor.type != '1':
                closed_list.add((competitor.F, competitor))
                current = competitor

                if current == goal:
                    break

                for adjacent in self.get_adjacents(current):

                    if (adjacent.F, adjacent) not in closed_list and adjacent.type != "1":
                        tentative_g = current.G + \
                            self.calculate_cost_to_movement(current, adjacent)

                        if (adjacent.F, adjacent) not in open_list or tentative_g < adjacent.G and not run or tentative_g > adjacent.G and run:
                            adjacent.father = current
                            adjacent.G = tentative_g
                            adjacent.H = self.calculate_distance_manhattan(
                                adjacent, goal)
                            adjacent.F = adjacent.G + adjacent.H

                            if (adjacent.F, adjacent) not in open_list:
                                heapq.heappush(
                                    open_list, (adjacent.F, adjacent))

    def resolve_WP(self, moviment_wolf = 1, moviment_prey = 1):
        while True:
            adjacents_wolf = self.multiple_adjacents(self.start)
            if adjacents_wolf == ":)":
                print("PEGO")
                break
            # os.system('cls')
            
            for index in range(moviment_prey):
                self.a_star_WP(start=self.end, goal=self.start, run=moviment_prey)
                move = self.reconstruct_path(side=self.start)[1]

                self.end.type = "0"
                self.end = move  
                self.end.type = "P" 
            
            for index in range(moviment_wolf):
                self.a_star_WP(start=self.start, goal=self.end)
                move = self.reconstruct_path()[1]
                
                self.start.type = "0" 
                self.start = move  
                self.start.type = "W" 

            self.show_board()
            time.sleep(1)

b = Board_WP()
b.create_for_WP()
b.resolve_WP()