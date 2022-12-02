from random import choices, randint, random, choice
from typing import List, Tuple, Callable

#Terminologies Definition
chromosome = List[int]
population = List[chromosome]
FitnessDS  = List[Tuple[chromosome, int]]
pairsList = List[Tuple[chromosome, chromosome]]

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


def selectionProcess(fds:FitnessDS, index:int)->pairsList:
    """ 
    It returns two parents from the set of candidates of the current generation based on their fitness.\n
    Index - Name\n
    0 - Roulette Selection\n
    1 - Rank Based Selection\n

    Args:
        fds (FitnssDS): It is a list of tuples, which has two elements: the chromoome and it's fitness

    Returns:
        pairsList (List[Tuple[chromosome,chromosome]]) : It returns the list of selected parents in a form of a list of tuples
    """
    def rouletteSelection(fds:FitnessDS)->pairsList:
        rouletteWheel=[]
        for i in fds:
            chromo, fitness = i
            rouletteWheel += [chromo]*fitness
        parentsList=[]
        for i in range((len(fds)//2 )+1):
            parent1 = choice(rouletteWheel)
            parent2 = choice(rouletteWheel)
            while parent1==parent2:
                parent2 = choice(rouletteWheel)
            parentsList.append(parent1, parent2)
        return parentsList
    
    def rankBasedSelection(fds:FitnessDS)->pairsList:
        rankDS = []
        fds.sort(key= lambda e:e[1])
        for i in range(len(fds)):
            chromo, fitness, rank = fds[i], i+1
            rankDS += [chromo]*rank
        parentsList=[]
        for i in range((len(fds)//2 )+1):
            parent1 = choice(rankDS)
            parent2 = choice(rankDS)
            while parent1==parent2:
                parent2 = choice(rankDS)
            parentsList.append(parent1, parent2)
        return parentsList

    selectionMethodList = [rouletteSelection, rankBasedSelection]
    if index < 0 or index > 1:
        raise IndexError("Wrong index selection for method.")

    return selectionMethodList[index](fds)
    

def calculateFitness(p:population)->FitnessDS:
    """
    It asks the fitness of the chromosome from the user, and then assignes it to the chromosome.

    Args:
        p (population): It is he list of chromosomes, or the population of indiviual solutions or candidates.

    Returns:
        FitnessDS: It is a list of individuals coupled with their individual fitness.
    """
    fitnessDS = []
    for i in p:
        print(f"For Chromosome: {chromosomeToString(i)}: ")
        fit = input("\tEnter your rating from 0 to 10: ")
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
        
        Index - Name\n
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
    if index < 0 or index > 3:
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

def termination()->bool:
    ask = input("Do you want to continue? (y/N): ")
    if ask=='y':
        return True
    return False
    

def simpleGeneticAlgorithm():
    #Initial Population Input
    try:
        chromosomeLength = int(input("Enter Size of Chromosome: "))
    except:
        print("There was some weird input, we would consider size = 10.")
        chromosomeLength = 10
    
    try:
        size = int(input("Enter Size of the Population: "))
    except:
        print("There was some weird input, we would consider population size = 10.")
        size = 10
    #Initializing the GA
    parentPopulation = initialPopulationGeneration(size = size, chromosomeLength = chromosomeLength)
    #GA Methodology until Termination
    terminationCriteria = False
    while not terminationCriteria:
        #Calculating Fitness
        fitDS = calculateFitness(population = parentPopulation)
        #Selection Criteria
        selectionIndex = int(input("Enter which Selecion Method you would like to implement: \n0 - Roulette Selection\n1 - Rank Based Selection: "))
        #Selection of parents
        pairsListofParents = selectionProcess(fds = fitDS, index = selectionIndex)
        #Creating the next generation
        nextGeneration=[]
        for i in pairsListofParents:
            child1, child2 = crossoverFunction(a = i[0], b = i[1])
            nextGeneration.append(child1)
            nextGeneration.append(child2)
        #Mutation Input
        try:
            probab = float(input("Enter probablity for mutation in the next generation: "))
        except:
            print("Invalid Input!\n We will consider probablity as 0.5")
        
        try:
            mutNum = int(input("Enter possible number of mutations in a particular chromosome: "))
        except: 
            print("Invalid Input! We will consider 2 mutations in a chromosome.")
        #Mutating each child in the next generation
        for nextChromo in nextGeneration:
            nextChromo = mutation(nextChromo, probab, mutNum)
        #Checking for termination criteria
        terminationCriteria = termination()
    
    



def main():
    GeneticAlgorithmProcess()



if __name__ == "__main__":
    main()