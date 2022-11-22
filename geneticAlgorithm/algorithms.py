from random import choices, randint
from typing import List, Tuple

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
    
    Work:
        Genarates a population of genomes, for the initial phase of the Genetic Algorithms.
    """
    return [[choices([0,1], k=genomeLength)] for _ in range(size)]

def selectionProcess():
    """
    
    """
    def calculateFitness():
        pass
    def selectMate():
        pass
    pass

def crossoverFunction():
    
    def singlePointCrossover(a:genome, b:genome)->Tuple[genome, genome]:
        if len(a)!=len(b):
            raise ValueError("Genomes are not of equal length.")
        cut = randint(0, len(b)-1)
        a,b = a[:cut] + b[cut:], b[:cut] + a[cut:]
        return a,b

    def twoPointCrossover(a:genome, b:genome)->Tuple[genome, genome]:
        if len(a)!=len(b):
            raise ValueError("Genomes are not of equal length.")
        p = randint(0, len(a)-1)
         
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