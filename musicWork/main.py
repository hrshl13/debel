from click import command, option, Choice
from createMusic import KEYS, SCALES, INSTRUMENTS, BITS_PER_NOTE
from algorithms import initialPopulationGeneration, calculateFitness, selectionProcess, crossoverFunction
from random import shuffle
"""
Inputs from User


3 types of Users:
    1. Laymen
    2. Music Enthusiasts
    3. GA Specialist

3 types of input:
    a) Laymen
        1. Mood? Happy, Sad
        2. Time(Default 16)
        3. Fast/Slow (Only 2 fixed bpms, 120 and 180)
        4. Instrument

    b) Music Enthusiasts
        1. Number of Bars
        2. Number of notes per bar? (Time Signature)
        3. BPM
        4. Key Note 
        5. Scale
        6. Scale Root (int)
        7. Pauses?
        8. Volume??
        9. Instrument

    c) GA Specialist
        1. Chromosome Length (would have to calculate stuff differently)
        2. Mood (Happy/Sad)
        3. Instrument
        4. Type of GA Evolution Strategy
        5. Population Size
        6. Selecion Method
        7. Type of Crossover
        8. Mutation %
        9. Number of Mutations
        
"""

@command
@option("--num-bars", default=8, prompt='Number of bars:', type=int)
@option("--num-notes", default=4, prompt='Notes per bar:', type=int)
@option("--num-steps", default=1, prompt='Number of steps:', type=int)
@option("--pauses", default=False, prompt='Introduce Pauses?', type=bool)
@option("--key", default="C", prompt='Key:', type=Choice(KEYS, case_sensitive=False))
@option("--scale", default="major", prompt='Scale:', type=Choice(SCALES, case_sensitive=False))
@option("--root", default=4, prompt='Scale Root:', type=int)
@option("--population-size", default=10, prompt='Population size:', type=int)
@option("--num-mutations", default=2, prompt='Number of mutations:', type=int)
@option("--mutation-probability", default=0.5, prompt='Mutations probability:', type=float)
@option("--bpm", default=60, prompt='BPM:', type=int)
def virtuosoMusic() -> None:
    pass


@command
@option("--mood", default="Happy", prompt='How is you mood?: ', type=Choice(["Happy", "Sad"],  case_sensitive=False))
@option("--time", default=16, type=int) # Preset to 16 seconds
@option("--speed", default=120, prompt='Enter speed in bpm:', type=Choice([120, 60]))
@option("--instrument", default="Piano", prompt='Choice of Instrument?: ', type=Choice(INSTRUMENTS), case_sensitive=False)
def laymanMusic(mood:str, time:int, speed:int, instrument:str) -> None:
    # 16 sconds ~ 4 notes per bar and 8 bars multiplied with BITS_PER_NOTE
    population = initialPopulationGeneration(5, 4*8*BITS_PER_NOTE)
    popID=0
    termination = False
    while not termination:
        shuffle(population)
        fitnessPopulation = calculateFitness(population)
        
    
    pass