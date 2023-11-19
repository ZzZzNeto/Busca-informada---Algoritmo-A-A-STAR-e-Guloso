import heapq


class Place:
    # types: 0 = Caminho, 1 = Parede, S = Inicio, # = Fim, P = Player
    def __init__(self, type, positionX, positionY, F=0, G=None, H=0, C=None):
        self.type = type
        self.F = F
        self.G = G
        self.H = H
        self.positionX = positionX
        self.positionY = positionY
        self.visited = False
        self.father = None

    def __lt__(self, other):
        return self.F < other.F

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

    def create_board_using_file(self):
        with open('template.txt') as txt:
            count_lines = 0
            for line in txt:
                if line.isspace():
                    continue
                self.places.append([])
                count_rows = 0
                for char in line:
                    if char != '\n':
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

    def get_adjacents(self, place):
        adjacents = []
        for line in self.places:
            for char in line:
                if char.positionX >= place.positionX - 1 and char.positionX <= place.positionX + 1 and char.positionY >= place.positionY - 1 and char.positionY <= place.positionY + 1 and char.type != '*' and char.type != 'S' and char.type != '-' and char.type != '1':
                    adjacents.append(char)

        return adjacents

    def calculate_cost_to_movement(self, current, end):
        current_positionX, current_positionY = current.positionX, current.positionY
        end_positionX, end_positionY = end.positionX, end.positionY

        distance_manhattan = abs(
            current_positionY - current_positionX) + abs(end_positionX - end_positionY)

        return distance_manhattan

    def calculate_distance_manhattan(self, current, end):
        return abs(current.positionX - end.positionX) + abs(current.positionY - end.positionY)

    def a_star(self):
        self.initialPosition.G = 0
        self.initialPosition.H = self.calculate_distance_manhattan(
            self.initialPosition, self.end)
        self.initialPosition.F = self.initialPosition.H + self.initialPosition.G

        open_list = [(self.initialPosition.F, self.initialPosition)]
        closed_list = set()
        current = self.initialPosition

        while open_list:
            f, competitor = heapq.heappop(open_list)

            if competitor and competitor.type != '1':
                closed_list.add((competitor.F, competitor))
                current = competitor

                if current == self.end:
                    break

                for adjacent in self.get_adjacents(current):

                    if (adjacent.F, adjacent) not in closed_list and adjacent.type != "1":
                        tentative_g = current.G + \
                            self.calculate_cost_to_movement(current, adjacent)

                        if (adjacent.F, adjacent) not in open_list or tentative_g < adjacent.G:
                            adjacent.father = current
                            adjacent.G = tentative_g
                            adjacent.H = self.calculate_distance_manhattan(
                                adjacent, self.end)
                            adjacent.F = adjacent.G + adjacent.H

                            if (adjacent.F, adjacent) not in open_list:
                                heapq.heappush(
                                    open_list, (adjacent.F, adjacent))

    def reconstruct_path(self):
        path = []
        current = self.end

        while current:
            path.append(current)
            current = current.father

        path.reverse()
        return path


b = Board()
b.create_board_using_file()
b.a_star()
a = b.reconstruct_path()
for i in a:
    print(i.positionX, i.positionY, i.type)
