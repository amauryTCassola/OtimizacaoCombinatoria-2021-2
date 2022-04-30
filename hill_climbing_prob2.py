import random

#struct/classe pra uma solução do problema
#Matriz X representando o caminho
#Array P representando os pesos
class Problem2Instance:
    def __init__(self, distances, demands, limits):
        self.distances = distances
        self.demands = demands
        self.limits = limits



#Função pra validação de solução
#Checa se os pesos respeitam as restruções dos problemas
def isSolution(candidate, instance):
    makeSolutionStartAtZero(candidate)
    n = len(instance.demands)
    curWeight = sum(instance.demands)
    for i in range(2,n):
        if curWeight > instance.limits[candidate[i]]:
            return False
        curWeight = curWeight - instance.demands[candidate[i]]
    return True

def makeSolutionStartAtZero(solution):
    while solution[0] != 0:
        first = solution.pop(0)
        solution.append(first)


def randomSolution(tsp):
    cities = list(range(len(tsp)))
    solution = []

    for i in range(len(tsp)):
        randomCity = cities[random.randint(0, len(cities) - 1)]
        solution.append(randomCity)
        cities.remove(randomCity)

    return solution

def routeLength(tsp, solution):
    routeLength = 0
    for i in range(len(solution)):
        routeLength += tsp[solution[i - 1]][solution[i]]
    return routeLength

#Função pra geração de vizinho aleatório
def getNeighbours(solution):
    neighbours = []
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            neighbour = solution.copy()
            neighbour[i] = solution[j]
            neighbour[j] = solution[i]
            yield neighbour #isso aqui faz a função funcionar como gerador de neighbours (assim não precisamos gerar a vizinhança toda, só um de cada vez, mas podemos iterar)
            #neighbours.append(neighbour)
    #return neighbours

#def getBestNeighbour(tsp, neighbours):
#    bestRouteLength = routeLength(tsp, neighbours[0])
#    bestNeighbour = neighbours[0]
#    for neighbour in neighbours:
#        currentRouteLength = routeLength(tsp, neighbour)
#        if currentRouteLength < bestRouteLength:
#            bestRouteLength = currentRouteLength
#            bestNeighbour = neighbour
#    return bestNeighbour, bestRouteLength

def getFirstImprovement(tsp, curSolution, neighbours):
    curSolutionLength = routeLength(tsp, curSolution)
    curNeighbour = next(neighbours)
    while curSolutionLength <= routeLength(tsp, curNeighbour):
        try:
            curNeighbour = next(neighbours)
        except StopIteration:
            return None
    return curNeighbour

#Função do Hill Climbing em si
#recebe uma instância do problema
def hillClimbing(tsp):
    currentSolution = randomSolution(tsp)
    neighbours = getNeighbours(currentSolution) #é um generator sobre o qual podemos iterar
    firstImprovement = getFirstImprovement(tsp, currentSolution, neighbours)

    while firstImprovement is not None: #firstImprovement só vai ser None quando nenhum dos vizinhos for melhor que a solução atual, significando que atingimos um pico
        neighbours.close() #necessário pq vamos criar outro generator pros vizinhos da nova solução
        currentSolution = firstImprovement
        neighbours = getNeighbours(currentSolution)
        firstImprovement = getFirstImprovement(tsp, currentSolution, neighbours)

    makeSolutionStartAtZero(currentSolution) #isso aqui é só pra ficar bonitinho mesmo

    return currentSolution, routeLength(tsp, currentSolution)



def main():
    tsp = [
        [0, 9, 6, 7, 100],
        [9, 0, 3, 100, 10],
        [6, 3, 0, 5, 4],
        [7, 100, 5, 0, 8],
        [100, 10, 4, 8, 0]
    ]

    print(hillClimbing(tsp))

if __name__ == "__main__":
    main()