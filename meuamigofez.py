import heapq

# import heapq

# class Node:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#         self.g = 0  # Custo do ponto inicial até este ponto
#         self.h = 0  # Custo estimado do ponto atual até o ponto final
#         self.f = 0  # Custo total (f = g + h)
#         self.parent = None  # Nó pai

# def heuristic(node, goal):
#     # Distância de Manhattan
#     return abs(node.x - goal.x) + abs(node.y - goal.y)

# def astar_search(start, goal, grid):
#     open_set = []
#     closed_set = set()

#     start_node = Node(start[0], start[1])
#     goal_node = Node(goal[0], goal[1])

#     heapq.heappush(open_set, (start_node.f, start_node))
    
#     while open_set:
#         current_node = heapq.heappop(open_set)[1]

#         if current_node.x == goal_node.x and current_node.y == goal_node.y:
#             path = []
#             while current_node:
#                 path.append((current_node.x, current_node.y))
#                 current_node = current_node.parent
#             return path[::-1]  # Inverte a lista para obter o caminho correto

#         closed_set.add((current_node.x, current_node.y))

#         for i, j in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
#             neighbor = Node(current_node.x + i, current_node.y + j)

#             if (
#                 0 <= neighbor.x < len(grid) and
#                 0 <= neighbor.y < len(grid[0]) and
#                 grid[neighbor.x][neighbor.y] != 1 and
#                 (neighbor.x, neighbor.y) not in closed_set
#             ):
#                 neighbor.g = current_node.g + 10 if i == 0 or j == 0 else 14  # Custo de movimento
#                 neighbor.h = heuristic(neighbor, goal_node)
#                 neighbor.f = neighbor.g + neighbor.h

#                 if (neighbor.f, neighbor) not in open_set:
#                     heapq.heappush(open_set, (neighbor.f, neighbor))
#                 else:
#                     # Se o novo caminho for melhor, atualize o nó na lista aberta
#                     for index, (f, node) in enumerate(open_set):
#                         if node.x == neighbor.x and node.y == neighbor.y and neighbor.g < node.g:
#                             open_set[index] = (neighbor.f, neighbor)
#                             break

#     return None  # Caminho não encontrado

# Exemplo de uso


# class Node:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#         self.g = 0  # Custo do ponto inicial até este ponto
#         self.h = 0  # Custo estimado do ponto atual até o ponto final
#         self.f = 0  # Custo total (f = g + h)
#         self.parent = None  # Nó pai
#         self.start = None
#         self.goal = None


#     def __lt__(self, other):
#         return self.f < other.f
# import numpy as np
class Place:
    #types: 0 = Caminho, 1 = Parede, S = Inicio, # = Fim, P = Player
    def __init__(self, type, positionX, positionY):
        self.type = type
        self.g = 0
        self.h = 0
        self.f = 0
        self.positionX = positionX
        self.positionY = positionY
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f
    
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
        # Distância de Manhattan
        return abs(place.positionX - self.end.positionX) + abs(place.positionY - self.end.positionY)

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

    def rearrange(self, list):
        minior = 0
        for i in list:
            print(i.f)
        pass
    def get_adjacents(self, place):
        adjacents = []
        for line in self.places:
            for char in line: 
                if char.positionX >= place.positionX - 1 and char.positionX <= place.positionX + 1 and char.positionY >= place.positionY - 1 and char.positionY <= place.positionY + 1 and char.type != '*' and char.type != 'S' and char.type != '-' and char.type != '1':
                    adjacents.append(char)
        
        return adjacents
    def astar_search(self):
       

#     heapq.heappush(open_set, (start_node.f, start_node))
        # while open_set:
        #     current_node = heapq.heappop(open_set)[1]
            
        #     if current_node.positionX == goal_node.positionX and current_node.positionY == goal_node.positionY:
        #         path = []
        #         while current_node:
        #             path.append((current_node.positionX, current_node.positionY))
        #             current_node = current_node.parent
        #         print(path[::-1])
        #         return path[::-1]  # Inverte a lista para obter o caminho correto

        #     closed_set.add((current_node.positionX, current_node.positionY))
        #     for i, j in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:

        #         if 0 <= current_node.positionX + i < len(self.places) and 0 <= current_node.positionY + j < len(self.places[0]):
        #             print(current_node.positionX, len(self.places),  current_node.positionY, len(self.places[0]))
        #             neighbor = self.places[current_node.positionX + i][current_node.positionY + j]
                    
        #             if (
        #                 self.places[neighbor.positionX][neighbor.positionY].type != '1' and
        #                 (neighbor.positionX, neighbor.positionY) not in closed_set
        #             ):
                        
                        
        #                 neighbor.g = current_node.g + 10 if i == 0 or j == 0 else 14  # Custo de movimento
        #                 neighbor.h = self.heuristic(neighbor)
        #                 neighbor.f = neighbor.g + neighbor.h
        #                 neighbor.parent = current_node

        #                 if neighbor not in open_set:
        #                     # print('ADICIONADO: ', self.places[neighbor.positionX][neighbor.positionY].type)
        #                     heapq.heappush(open_set, (neighbor.f, neighbor))

        #                 else:
        #                     # Se o novo caminho for melhor, atualize o nó na lista aberta
        #                     for existing_node in open_set:
        #                         if existing_node.positionX == neighbor.positionX and existing_node.positionY == neighbor.positionY and neighbor.g < existing_node.g:
        #                             existing_node.g = neighbor.g
        #                             existing_node.parent = current_node
        #                             break

                

        #         else:
        #             continue

        # return None  # Caminho não encontrado
        open_set = []
        closed_set = set()
        
        # self.rearrange(open_set)

        start_node = self.initialPosition
        goal_node = self.end

        heapq.heappush(open_set, (start_node.f, start_node))
        
        while len(open_set) > 0:
            current_node = heapq.heappop(open_set)[1]
            print(current_node.type, current_node.positionX, current_node.positionY)
            if current_node.positionX == goal_node.positionX and current_node.positionY == goal_node.positionY:
                path = []
                print('eu entrei')
                while current_node:
                    path.append((current_node.x, current_node.y))
                    current_node = current_node.parent
                print(path[::-1])
                return path[::-1]  # Inverte a lista para obter o caminho correto

            closed_set.add((current_node.positionX, current_node.positionY))

            for i, j in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                if 0 <= current_node.positionX + i < len(self.places) and 0 <= current_node.positionY + j < len(self.places[0]):
                    neighbor = self.places[current_node.positionX + i][current_node.positionY + j]

                    if (
                        self.places[neighbor.positionX][neighbor.positionY].type != '1' and
                        (neighbor.positionX, neighbor.positionY) not in closed_set
                    ):
                        neighbor.g = current_node.g + 10 if i == 0 or j == 0 else 14  # Custo de movimento
                        neighbor.h = self.heuristic(neighbor)
                        neighbor.f = neighbor.g + neighbor.h

                        if (neighbor.f, neighbor) not in open_set:
                            print('entrei sim prexeco')
                            heapq.heappush(open_set, (neighbor.f, neighbor))
                        else:
                            # Se o novo caminho for melhor, atualize o nó na lista aberta
                            for index, (f, node) in enumerate(open_set):
                                if node.positionX == neighbor.positionX and node.positionY == neighbor.positionY and neighbor.g < node.g:
                                    open_set[index] = (neighbor.f, neighbor)
                                    break
                else:
                    continue
            for a, i in closed_set:
                print(a, i)
            return None  # Caminho não encontrado

if __name__ == "__main__":
    b = Board()
    b.create_board_using_file()
    b.show_board()
    b.astar_search()

# lista_de_listas = [[1, 2, 3],
#                    [4, 5, 6],
#                    [7, 8, 9]]

# # Obter a altura e a largura da lista de listas
# altura = len(lista_de_listas)
# largura = len(lista_de_listas[0]) if lista_de_listas else 0  # Considera 0 se a lista estiver vazia

# # Exibir os resultados
# print(f"Altura da lista de listas: {altura}")
# print(f"Largura da lista de listas: {largura}")