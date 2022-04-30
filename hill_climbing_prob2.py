import random
import sys
from read_text_file import *

#struct/classe pra uma solução do problema
#Matriz X representando o caminho
#Array P representando os pesos
class Problem2Instance:
    def __init__(self, distances, demands, limits):
        self.distances = distances
        self.demands = demands
        self.limits = limits
        self.limits[0] = sum(self.demands)
        self.n = len(limits)


#Função pra validação de solução
#Checa se os pesos respeitam as restruções dos problemas
def isSolution(candidate, instance):
    makeSolutionStartAtZero(candidate)
    curWeight = sum(instance.demands)
    for i in range(len(candidate)):
        if curWeight > instance.limits[candidate[i]] or curWeight < instance.demands[candidate[i]]:
            return False
        curWeight = curWeight - instance.demands[candidate[i]]
    return True

def makeSolutionStartAtZero(solution):
    while solution[0] != 0:
        first = solution.pop(0)
        solution.append(first)


def randomTSPSolution(tsp):
    cities = list(range(len(tsp)))
    solution = []

    for i in range(len(tsp)):
        randomCity = cities[random.randint(0, len(cities) - 1)]
        solution.append(randomCity)
        cities.remove(randomCity)

    return solution

def randomSolution(instance):
    randomSol = randomTSPSolution(instance.distances)
    while isSolution(randomSol, instance) == False:
        randomSol = randomTSPSolution(instance.distances)
    return randomSol

def routeLength(problemInstance, solution):
    routeLength = 0
    for i in range(len(solution)):
        routeLength += problemInstance.distances[solution[i - 1]][solution[i]]
    return routeLength

#Função pra geração de vizinho aleatório
def getNeighbours(solution, instance):
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            neighbour = solution.copy()
            neighbour[i] = solution[j]
            neighbour[j] = solution[i]
            if isSolution(neighbour, instance):
                yield neighbour #isso aqui faz a função funcionar como gerador de neighbours (assim não precisamos gerar a vizinhança toda, só um de cada vez, mas podemos iterar)
            else:
                continue

def getFirstImprovement(problemInstance, curSolution, neighbours):
    curSolutionLength = routeLength(problemInstance, curSolution)
    curNeighbour = next(neighbours)
    while curSolutionLength <= routeLength(problemInstance, curNeighbour):
        try:
            curNeighbour = next(neighbours)
        except StopIteration:
            return None
    return curNeighbour


#Função do Hill Climbing em si
#recebe uma instância do problema
def hillClimbing(problemInstance):
    currentSolution = randomSolution(problemInstance)
    neighbours = getNeighbours(currentSolution, problemInstance) #é um generator sobre o qual podemos iterar
    firstImprovement = getFirstImprovement(problemInstance, currentSolution, neighbours)

    while firstImprovement is not None: #firstImprovement só vai ser None quando nenhum dos vizinhos for melhor que a solução atual, significando que atingimos um pico
        neighbours.close() #necessário pq vamos criar outro generator pros vizinhos da nova solução
        currentSolution = firstImprovement
        neighbours = getNeighbours(currentSolution, problemInstance)
        firstImprovement = getFirstImprovement(problemInstance, currentSolution, neighbours)

    makeSolutionStartAtZero(currentSolution) #isso aqui é só pra ficar bonitinho mesmo

    return currentSolution, routeLength(problemInstance, currentSolution)

def main():

    n = len(sys.argv)
    if n < 3:
        exit()
    
    path = sys.argv[1]
    iterations = int(sys.argv[2])

    distances, demands, limits = InstanceFromTextFile(path)

    instance = Problem2Instance(distances, demands, limits)

    results = []

    for i in range(iterations):
        results.append(hillClimbing(instance))

    bestResult = results[0][1]
    bestPath = []

    for i in range(iterations):
        curResult = results[i][1]
        if curResult < bestResult:
            bestResult = curResult
            bestPath = results[i][0]

    print(bestPath)
    print(bestResult)

if __name__ == "__main__":
    main()