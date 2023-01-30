from pyo import Events, EventScale, EventSeq, Metro, Sine, CosTable, Iter, TrigEnv, Server
from midiutil import MIDIFile
from typing import List, Dict
import os
from music21.instrument import AcousticGuitar, Piano, Organ, AltoSaxophone, Flute
from music21 import converter
from .algorithms import chromosomeToString, chromosome
BITS_PER_NOTE=4
"""
Number of bits assigned for a single note 
"""


# The list of Scales, Keys and Instruments as allowed by the EventScale class of pyo
SCALES = ["major", "minorH", "minorM", "ionian", "dorian", "phrygian", "lydian", "mixolydian", "aeolian", "locrian", "wholeTone", "majorPenta", "minorPenta", "egyptian", "majorBlues", "minorBlues","minorHungarian"]

KEYS = ["C", "C#", "Db", "D", "D#", "Eb", "E", "F", "F#", "Gb", "G", "G#", "Ab", "A", "A#", "Bb", "B"]

INSTRUMENTS = [AcousticGuitar.__name__, Piano.__name__, Organ.__name__, AltoSaxophone.__name__, Flute.__name__]

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

def eventDSCreation(numOctaves:int,numTracks:int,numBars:int, gene: chromosome, isPause:bool, key:str, scale:str, scaleRoot:float, sig:str)->Dict:
    
    notesPerBar = TIME_SIGNATURE_TO_BEATS[sig]
    # If the Time Signature is 5/4, implement Dave Brubeck Quartet's "Take Five", 5/4(3/4 + 2/4) Time Signature. 
    takeFive = False 
    if notesPerBar==5:
        takeFive=True

    notes=[]
    for i in range(numBars*notesPerBar):
        notes.append(gene[i*BITS_PER_NOTE : i*BITS_PER_NOTE + BITS_PER_NOTE])
    scl = EventScale(root=key, scale=scale, first=scaleRoot, octaves=numOctaves)

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
            noteLength = 4 / float(3)
        elif counter>=3 and counter<5 and takeFive:
            noteLength = 4 / float(2)
        
        if not isPause:
            # A kind of flag to introduce pauses in between
            integer = int(integer % pow(2, BITS_PER_NOTE - 1))
        
        # If the note is a pause note
        if integer >= pow(2, BITS_PER_NOTE - 1):
            eventDS["pitch"] += [0]
            eventDS["volume"] += [0]
            eventDS["beat"] += [noteLength]
        
        # Not a pause note
        else:
            # If there are two notes of the same pitch simultaneously,
            if len(eventDS["pitch"]) > 0 and eventDS["pitch"][-1] == integer and not takeFive:
                # Just increase the note length of the previous note
                eventDS["beat"][-1] += noteLength
            else:
                eventDS["pitch"] += [integer]
                eventDS["volume"] += [127]
                eventDS["beat"] += [noteLength]
        if takeFive:
            counter+=1
    
    steps = []
    for step in range(numTracks):
        steps.append([int(scl[(note+step*2) % len(scl)]) for note in eventDS["pitch"]])

    eventDS["pitch"] = steps
    return eventDS


def saveMidi(filename:str, numOctaves:int, numTracks:int,numBars:int, gene:chromosome, isPause:bool, key:str, scale:str, scaleRoot:float, sig:str,bpm:int):

    eventDS = eventDSCreation(numOctaves, numTracks, numBars, gene, isPause, key, scale, scaleRoot, sig)
    if len(eventDS["pitch"][0]) != len(eventDS["beat"]) or len(eventDS["pitch"][0]) != len(eventDS["volume"]):
        raise ValueError
    mf = MIDIFile(1)
    print(eventDS["volume"])
    track = 0
    channel = 0

    time = 0.0
    mf.addTrackName(track, time, "Sample Track")
    mf.addTempo(track, time, bpm)

    for i, vol in enumerate(eventDS["volume"]):
        if vol > 0:
            for step in eventDS["pitch"]:
                mf.addNote(track, channel, step[i], time, eventDS["beat"][i], vol)
        time += eventDS["beat"][i]
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as f:
        mf.writeFile(f)
    
def changeInstrument(midiFilePath:str, oldInstrument:str, newInstrument:str):
    newInstrumentClass = eval(newInstrument)
    s = converter.parse(midiFilePath)
    for el in s.recurse():
        if 'Instrument' in el.classes or oldInstrument in el.classes: 
            el.activeSite.replace(el, newInstrumentClass())
        s.write("midi", midiFilePath)
    

def metronome(bpm: int):
    """
    Plays a Metronome (using pyo) the input beats per minute when called.

    Args:
        bpm (int): Beats Per Minute

    Returns:
        Would return a Sine obj, using out method, which will play the Metronome on the pyo server 
    """
    met = Metro(time=1 / (bpm / 60.0)).play()
    t = CosTable([(0, 0), (50, 1), (200, .3), (500, 0)])
    amp = TrigEnv(met, table=t, dur=.25, mul=15)
    freq = Iter(met, choice=[660, 440, 440, 440])
    return Sine(freq=freq, mul=amp).mix(2).out()

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