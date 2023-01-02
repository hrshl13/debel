from pyo import *
from midiutil import MIDIFile
from typing import List
scales = ["major", "minorH", "minorM", "ionian", "dorian", "phrygian", "lydian", "mixolydian", "aeolian", "locrian", "wholeTone", "majorPenta", "minorPenta", "egyptian", "majorBlues", "minorBlues","minorHungarian"]

keys = ["C", "C#", "Db", "D", "D#", "Eb", "E", "F", "F#", "Gb", "G", "G#", "Ab", "A", "A#", "Bb", "B"]

def bitsToInteger(bits:List[int])->int:
    integer=0
    for index, bit in reversed(list(enumerate(bits))):
        integer+= bit * (2**index)
    return integer

print(bitsToInteger([0,0,1,0]))
print(bitsToInteger([0,1,1,0]))
print(bitsToInteger([1,1,1,0]))