from random import choices, randint, random
from typing import List, Tuple, Callable

#Terminologies Definition
chromosome = List[int]
population = List[chromosome]
crossoverMethod = Callable[[chromosome, chromosome], Tuple[chromosome , chromosome]]

#Common Methods
def chromosomeToString(a:chromosome)->str:
    """
    Parameter
        1. a: chromosome(list of int) 
    Returns
        a string of 1s and 0s
    Work
        It converts the list of binary bits into a bit string
    """
    s = "".join(a)
    return s

#Algorithm Methods
def initialPopulationGeneration(size:int, chromosomeLength:int)->population:
    """
    Parameters
        1. size: size of population in int 
        2. chromosomeLength: length of chromosome in int 
    
    Returns
        list of chromosomes 
    
    Work
        Genarates a population of chromosomes, for the initial phase of the Genetic Algorithm.
    """
    return [[choices([0,1], k=chromosomeLength)] for _ in range(size)]

def selectionProcess():
    """
    Parameters
    
    Returns

    Work
    """
    pass

def calculateFitness():
    pass

def crossoverFunction(a:chromosome, b:chromosome,index:int):
    
    def singlePointCrossover(a:chromosome, b:chromosome)->Tuple[chromosome, chromosome]:
        """
        Paramters
            1. a: chromosome(list of int)
            2. b: chromosome(list of int)
        
        Returns
            a tuple of chromosomes
        
        Work
            We take two chromosomes and cut them at the same random point.
            After that, we switch the two parts of the chromosomes in such a way that the length of the chromosome remains unchanged from the original length.
            Also, note the fact that the length of both the chromosomes remain equal throughout the process.
        """
        if len(a)!=len(b):
            raise ValueError("chromosomes are not of equal length.")
        cut = randint(0, len(b)-1)
        a,b = a[:cut] + b[cut:], b[:cut] + a[cut:]
        return a,b

    def twoPointCrossover(a:chromosome, b:chromosome)->Tuple[chromosome, chromosome]:
        """
        Paramters
            1. a: chromosome(list of int)
            2. b: chromosome(list of int)
        
        Returns
            a tuple of chromosomes
        
        Work
            We take two chromosomes and cut them at two same points decided randomly.
            After that, we are left with three parts of the two chromosomes each. We then swap the middle parts of the two, to get two chromosomes in return of the same length as the original chromosomes.
            Also, note the fact that the length of both the chromosomes remain equal throughout the process.
        """
        if len(a)!=len(b):
            raise ValueError("chromosomes are not of equal length.")
        p = randint(0, len(a)-1)
        if p!=0:
            q=randint(0,p)
            aStart, aMiddle, aEnd = a[:q], a[q:p], a[p:]
            bStart, bMiddle, bEnd = b[:q], b[q:p], b[p:]        
        else:
            q=randint(p,len(a))
            aStart, aMiddle, aEnd = a[:p], a[p:q], a[q:]
            bStart, bMiddle, bEnd = b[:p], b[p:q], b[q:]
        
            print(
            f"Two Point Crossover\n"+
            f"Original chromosomes\n a: {chromosomeToString(a)}\n b: {chromosomeToString(b)}\n"+
            f"aStart: {chromosomeToString(aStart)}\t aMiddle: {chromosomeToString(aMiddle)}\t aEnd: {chromosomeToString(aEnd)}\n"+
            f"bStart: {chromosomeToString(bStart)}\t bMiddle: {chromosomeToString(bMiddle)}\t bEnd: {chromosomeToString(bEnd)}\n"
        )
        a,b = aStart + bMiddle + aEnd, bStart + aMiddle + bEnd    
        return a,b

    def multiPointCrossover():

        pass

    def uniformCrossover(a:chromosome, b:chromosome)->Tuple[chromosome, chromosome]:
        # def uCwithTossing(a: chromosome, b:chromosome)->Tuple[chromosome, chromosome]:
        coinToss = [choices([0,1],k=len(a))]
        offspring1 = [b[i] if coinToss[i] else a[i] for i in range(len(coinToss))]
        offspring2 = [a[i] if coinToss[i] else b[i] for i in range(len(coinToss))]
        return offspring1, offspring2
        
        # def uCwithCrossoverMask(a:chromosome, b:chromosome)->Tuple[chromosome, chromosome]:
        crossoverMask = [choices([0,1], k=len(a))]
        offspring1=[a[i] if crossoverMask[i] else b[i] for i in range(len(crossoverMask))]
        offspring2=[b[i] if crossoverMask[i] else a[i] for i in range(len(crossoverMask))]
        return offspring1, offspring2

    crossoverMethodList = [singlePointCrossover(a,b), twoPointCrossover(a,b), multiPointCrossover(), uniformCrossover(a,b)]
    pass

def mutation( g:chromosome,probablity:float, numberOfMutations:int)->chromosome:
    """
    Parameters
        1. g: chromosome(list of int)
        2. probablity: probability of a gene to mutate in float
        3. numberOfMutations: 
    Returns

    Work

    """
    for i in range(numberOfMutations):
        index = randint(0,len(g))
        g[index] = abs(g[index] - 1) if probablity<random() else g[index]
    return g

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
    GeneticAlgorithmProcess()



if __name__ == "__main__":
    main()