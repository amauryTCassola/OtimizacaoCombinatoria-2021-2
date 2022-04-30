import random

#struct/classe pra uma solução do problema
#Matriz X representando o caminho
#Array P representando os pesos
class Problem2Instance:
    def __init__(self, distances, demands, limits):
        self.distances = distances
        self.demands = demands
        self.limits = limits



#Função pra validação de solução (tem que ver se é factível)
#Checa se os pesos fazem sentido
def isSolution(candidate, instance):
    makeSolutionStartAtZero(candidate)
    n = instance.demands.length
    curWeight = sum(instance.demands)
    for i in 1:instance.
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

#Função pra geração de vizinho aleatório (ou da vizinhança toda?)
#iterator? Algo assim? Pesquisar sobre
def getNeighbours(solution):
    neighbours = []
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            neighbour = solution.copy()
            neighbour[i] = solution[j]
            neighbour[j] = solution[i]
            yield neighbour
            #neighbours.append(neighbour)
    #return neighbours

def getBestNeighbour(tsp, neighbours):
    bestRouteLength = routeLength(tsp, neighbours[0])
    bestNeighbour = neighbours[0]
    for neighbour in neighbours:
        currentRouteLength = routeLength(tsp, neighbour)
        if currentRouteLength < bestRouteLength:
            bestRouteLength = currentRouteLength
            bestNeighbour = neighbour
    return bestNeighbour, bestRouteLength

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
#recebe uma instância do problema (talvez o k da k-exchange possa ser um parâmetro tbm?)
def hillClimbing(tsp):
    currentSolution = randomSolution(tsp)
    neighbours = getNeighbours(currentSolution)
    firstImprovement = getFirstImprovement(tsp, currentSolution, neighbours)

    while firstImprovement is not None:
        neighbours.close()
        currentSolution = firstImprovement
        neighbours = getNeighbours(currentSolution)
        firstImprovement = getFirstImprovement(tsp, currentSolution, neighbours)

    makeSolutionStartAtZero(currentSolution)

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