from pyo import Events, EventScale, EventSeq, Metro, Sine, CosTable, Iter, TrigEnv
from midiutil import MIDIFile
from typing import List, Dict
from sys import path
from os import makedirs, path
from music21.instrument import AcousticGuitar, Piano, Organ, AltoSaxophone, Choir
from music21 import converter
path.insert(0, "C:/Users/Admin/Desktop/Codes/TYPROJECT/debel/geneticAlgorithm")
from geneticAlgorithm.algorithms import chromosomeToString, chromosome


BITS_PER_NOTE=4
"""
Number of bits assigned for a single note 
"""

"""
Inputs from User


3 types of Users:
    1. Laymen
    2. Music Enthusiasts
    3. GA Specialist

3 types of input:
    a) Laymen
        1. Mood? Happy, Sad
        2. Time (in seconds)
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


# The list of Scales and Keys as allowed by the EventScale class of pyo
SCALES = ["major", "minorH", "minorM", "ionian", "dorian", "phrygian", "lydian", "mixolydian", "aeolian", "locrian", "wholeTone", "majorPenta", "minorPenta", "egyptian", "majorBlues", "minorBlues","minorHungarian"]

KEYS = ["C", "C#", "Db", "D", "D#", "Eb", "E", "F", "F#", "Gb", "G", "G#", "Ab", "A", "A#", "Bb", "B"]

TIME_SIGNATURE_TO_BEATS = {
    "2/4" : 2, 
    "3/4" : 3,
    "4/4" : 4,
    "5/4" : 5,
}

def listToString(l:list)->str:
    """
    Creates a string out of the contents of list

    Args:
        l (list): List of objects that can be converted to string with str function.

    Returns:
        str: returns in the format (...)
    """
    string = "("
    for i in range(len(l)):
        if i!=len(l)-1:
            string += str(l[i]) + ", "
        else:
            string += str(l[i])
    string += ")"
    return string

def bitsToInteger(bits:List[int])->int:
    """
    Returns the integer to input list of bits

    Args:
        bits (List[int]): List of 0s and 1s

    Returns:
        int: The decimal representationof that  binary number
    """
    bitString = chromosomeToString(bits)
    return int(bitString, 2)




def eventDSCreation(numBars:int, gene: chromosome, isPause:bool, key:str, scale:str, scaleRoot:int, sig:str)->Dict:
    
    notesPerBar = TIME_SIGNATURE_TO_BEATS[sig]
    # If the Time Signature is 5/4, implement Dave Brubeck Quartet's "Take Five" 5/4 
    takeFive = False 
    if notesPerBar==5:
        takeFive=True

    notes=[]
    for i in range(numBars*notesPerBar):
        notes.append(gene[i*BITS_PER_NOTE : i*BITS_PER_NOTE + BITS_PER_NOTE])
    scl = EventScale(root=key, scale=scale, first=scaleRoot)

    eventDS = {
        "pitch":[],
        "volume":[],
        "beat":[]
    }
    noteLength = 4 / float(notesPerBar)
    counter=0
    for note in notes:
        integer = bitsToInteger(note)
        #if we introduce pausing, the beat will continue, but it will have a null note and a volume of zero
        if counter==5 and takeFive:
            counter=0
        if counter<3 and takeFive:
            note_length = 4 / float(3)
        elif counter>=3 and counter<5 and takeFive:
            note_length = 4 / float(2)
        
        if not isPause:
            # A kind of flag to introduce pauses in between
            integer = int(integer % pow(2, BITS_PER_NOTE - 1))
        
        # If the note is a pause note
        if integer >= pow(2, BITS_PER_NOTE - 1):
            eventDS["pitch"] += [0]
            eventDS["volume"] += [0]
            eventDS["beat"] += [note_length]
        
        # Not a pause note
        else:
            # If there are two notes of the same pitch simultaneously,
            if len(eventDS["pitch"]) > 0 and eventDS["pitch"][-1] == integer:
                # Just increase the note length of the previous note
                eventDS["beat"][-1] += note_length
            else:
                eventDS["pitch"] += [integer]
                eventDS["volume"] += [127]
                eventDS["beat"] += [note_length]
        if takeFive:
            counter+=1

    return eventDS

def eventCreation(numBars:int, gene: chromosome, isPause:bool, key:str, scale:str, scaleRoot:str, sig:str, bpm):
    eventDS = eventDSCreation(numBars, gene, isPause, key, scale, scaleRoot, sig)
    listOfEvents=[]
    for line in eventDS["pitch"]:
        listOfEvents.append( 
            Events(
                midinote=EventSeq(line, occurrences=1),
                midivel=EventSeq(eventDS["velocity"], occurrences=1),
                beat=EventSeq(eventDS["beat"], occurrences=1),
                attack=0.001,
                decay=0.05,
                sustain=0.5,
                release=0.005,
                bpm=bpm
            )
            )
    return listOfEvents

def metronome(bpm: int):
    met = Metro(time=1 / (bpm / 60.0)).play()
    t = CosTable([(0, 0), (50, 1), (200, .3), (500, 0)])
    amp = TrigEnv(met, table=t, dur=.25, mul=15)
    freq = Iter(met, choice=[660, 440, 440, 440])
    return Sine(freq=freq, mul=amp).mix(2).out()


def saveMidi(filename:str, numBars:int, gene:chromosome, isPause:bool, key:str, scale:str, scaleRoot:int, sig:str,bpm:int):

    eventDS = eventDSCreation(numBars, gene, isPause, key, scale, scaleRoot, sig)
    if len(eventDS["pitch"][0]) != len(eventDS["beat"]) or len(eventDS["pitch"][0]) != len(eventDS["volume"]):
        raise ValueError

    mf = MIDIFile(1)

    track = 0
    channel = 0

    time = 0.0
    mf.addTrackName(track, time, "Sample Track")
    mf.addTempo(track, time, bpm)

    for i, vel in enumerate(eventDS["volume"]):
        if vel > 0:
            for step in eventDS["pitch"]:
                mf.addNote(track, channel, step[i], time, eventDS["beat"][i], vel)

        time += eventDS["beat"][i]

    makedirs(path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as f:
        mf.writeFile(f)
    
def changeInstrument(midiFilePath:str, oldInstrument:str, newInstrument:str):
    newInstrumentClass = eval(newInstrument)
    s = converter.parse(midiFilePath)
    for el in s.recurse():
        if 'Instrument' in el.classes or oldInstrument in el.classes: 
            el.activeSite.replace(el, newInstrumentClass())
        s.write("midi", midiFilePath)
    
