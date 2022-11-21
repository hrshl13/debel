from random import choices
from typing import List

#Terminologies Definition
genome = List[int]
population = List[genome]



def initialPopulationGeneration(size:int, genomeLength:int)->population:
    """
    Parameters
        1. genomeLength: length of genome in int 
        2. size: size of population in int 
    
    Returns
        list of genomes 
    """
    return [[choices([0,1], k=genomeLength)] for _ in range(size)]

def selectionProcess():
    def calculateFitness():
        pass
    def selectMate():
        pass
    pass

def crossoverFunction():
    
    def singlePointCrossover():
        pass

    def twoPointCrossover():
        pass

    def multiPointCrossover():
        pass
    pass

def mutation():
    pass

def termination():
    pass


def GeneticAlgorithmProcess():
    initialPopulationGeneration()
    terminationCriteria = False
    while not terminationCriteria:
        selectionProcess()
        crossoverFunction()
        mutation()
    termination()
    pass



def main():
    pass



if __name__ == "__main__":
    main()