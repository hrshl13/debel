from random import choices, randint, random, choice
from typing import List, Tuple, Callable

#Terminologies Definition
chromosome = List[int]
population = List[chromosome]
crossoverMethod = Callable[[chromosome, chromosome], Tuple[chromosome , chromosome]]
FitnessDS  = List[Tuple[chromosome, int]]

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
    Genarates a population of chromosomes, for the initial phase of the Genetic Algorithm.
    
    Args:
        size: size of population in int 
        chromosomeLength: length of chromosome in int 
    
    Returns:
        list of chromosomes 
    """
    return [[choices([0,1], k=chromosomeLength)] for _ in range(size)]


def selectionProcess(fds:FitnessDS, index:int)->Tuple[chromosome,chromosome]:
    """ 
    It returns two parents from the set of candidates of the current generation based on their fitness.

    Args:
        fds (FitnssDS): It is a list of tuples, which has two elements: the chromoome and it's fitness

    Returns:
        Tuple[chromosome,chromosome]: It returns the selected parents in a form of a tuple
    """
    def rouletteSelection(fds:FitnessDS)->Tuple[chromosome, chromosome]:
        rouletteWheel=[]
        for i in fds:
            chromo, fitness = i
            rouletteWheel += [chromo]*fitness
        parent1 = choice(rouletteWheel)
        parent2 = choice(rouletteWheel)
        while parent1==parent2:
            parent2 = choice(rouletteWheel)
        return parent1, parent2
    
    def rankBasedSelection(fds:FitnessDS):
        rankDS = []
        fds.sort(key= lambda e:e[1])
        for i in range(len(fds)):
            chromo, fitness, rank = fds[i], i+1
            rankDS += [chromo]*rank
        parent1 = choice(rankDS)
        parent2 = choice(rankDS)
        while parent1==parent2:
            parent2 = choice(rankDS)
        return parent1, parent2

    selectionMethodList = [rouletteSelection, rankBasedSelection]
    if index < 0:
        raise IndexError("Wrong index selection for method.")

    return selectionMethodList[index](fds)
    

def calculateFitness(p:population)->List[Tuple[chromosome, int]]:
    """
    It asks the fitness of the chromosome from the user, and then assignes it to the chromosome.
    """
    fitnessDS = []
    for i in p:
        fit = input("Enter your rating from 0 to 10: ")
        try:
            fit = int(fit)
        except ValueError:
            print("Your rating was rejected due to inappropriate input. We would consider this rating to be zero.")
            fit=0
        fitnessDS.append((i,fit))        
    return fitnessDS


def crossoverFunction(a:chromosome, b:chromosome,index:int) -> Tuple[chromosome, chromosome]:
    """
    We take two parent chromosomes and perform certain methods on them such that they produce two child chromosomes.

    Args:
        a: a chromosome (list of int) 
        b: a chromosome (list of int) 
        index: int
        index specifies which type of Crossover do we want to perform.
        
        Values - Names\n
        0 - Single Point Crossover\n
        1 - Two Point Crossover\n
        2 - Multi Point Crossover\n
        3 - Uniform Crossover

    Returns:
        a tuple of chromsomes
    """
    
    def singlePointCrossover(a:chromosome, b:chromosome)->Tuple[chromosome, chromosome]:
        """
        We take two chromosomes and cut them at the same random point.
        After that, we switch the two parts of the chromosomes in such a way that the length of the chromosome remains unchanged from the original length.
        Also, note the fact that the length of both the chromosomes remain equal throughout the process.

        Args:
            a: chromosome(list of int)
            b: chromosome(list of int)
        
        Returns:
            a tuple of chromosomes
        """
        if len(a)!=len(b):
            raise ValueError("Chromosomes are not of equal length.")
        cut = randint(0, len(b)-1)
        a,b = a[:cut] + b[cut:], b[:cut] + a[cut:]
        return a,b

    def twoPointCrossover(a:chromosome, b:chromosome)->Tuple[chromosome, chromosome]:
        """
        We take two chromosomes and cut them at two same points decided randomly.
        After that, we are left with three parts of the two chromosomes each. We then swap the middle parts of the two, to get two chromosomes in return of the same length as the original chromosomes.
        Also, note the fact that the length of both the chromosomes remain equal throughout the process.
        
        Args:
            a: chromosome(list of int)
            b: chromosome(list of int)
        
        Returns:
            a tuple of chromosomes
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

    def multiPointCrossover(a:chromosome, b:chromosome) -> Tuple[chromosome, chromosome]:
        """
        We take 2 chromosomes and cut them into random chunks, and then swap out alternative chunks with one another.

        Args:
            a: a chromosome(list of int)
            b: a chromosome(list of int)

        Returns:
            a tuple of chromsomes
        """
        cutList = []
        times = randint(1,len(a)-1)
        for i in range(times):
            r = randint(1, len(a)-2)
            if r not in cutList:
                cutList.append(r)
        cutList.sort()
        for cut in cutList:
            a,b = a[:cut] + b[cut:], b[:cut] + a[cut:]
        return a,b

    def uniformCrossover(a:chromosome, b:chromosome)->Tuple[chromosome, chromosome]:
        """
        We take two chromosomes and interchange each bit of the two parent chromsomes to create child chromosomes using a coin toss (or a randomizer).

        Args:
            a: a chromosome (list of int)
            b: a chromosome (list of int)

        Returns:
            a tuple of chromosomes
        """
        coinToss = [choices([0,1],k=len(a))]
        offspring1 = [b[i] if coinToss[i] else a[i] for i in range(len(coinToss))]
        offspring2 = [a[i] if coinToss[i] else b[i] for i in range(len(coinToss))]
        return offspring1, offspring2
        

    crossoverMethodList = [singlePointCrossover, twoPointCrossover, multiPointCrossover, uniformCrossover]
    if index < 0:
        raise IndexError("Wrong index selection for method.")

    return crossoverMethodList[index](a,b)


def mutation( g:chromosome,probablity:float, numberOfMutations:int)->chromosome:
    """
    We change one or many genes (bit) based on a certain probability from 0 to 1 or vice-versa.

    Args:
        g: chromosome(list of int)
        probablity: probability of a gene to mutate in float
        numberOfMutations: number of genes to be changed
    
    Returns:
        a chromosome
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