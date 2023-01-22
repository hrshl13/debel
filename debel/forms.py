from django.forms import Form, ChoiceField, IntegerField, BooleanField, FloatField
from django.forms.widgets import RadioSelect

# Extra Information and choice fields 
mu = "\u03BC"
lamda = "\u03BB"
evoChoices = [
    (0, f"({mu} + {lamda})"),
    (1, f"({mu}, {lamda})")
]

scaleChoices = [
("major", "Major"),
("minorH", "Minor Harmonic"),
("minorM", "Minor Melodic"),
("ionian", "Ionian"),
("dorian", "Dorian"),
("phrygian", "Phrygian"),
("lydian", "Lydian"),
("mixolydian", "Mixolydian"),
("aeolian", "Aeolian"),
("locrian", "Locrian"),
("wholeTone", "Whole Tone"),
("majorPenta", "Major Penta"),
("minorPenta", "Minor Penta"),
("egyptian", "Egyptian"),
("majorBlues", "Major Blues"),
("minorBlues", "Minor Blues"),
("minorHungarian", "Minor Hungarian")]

keyChoices = [
("C","C"),
("E","E"),
("D","D"),
("F","F"),
("G","G"),
("A","A"),
("B","B"),
("C#","C#"),
("Db","Db"),
("D#","D#"),
("Eb","Eb"),
("F#","F#"),
("Gb","Gb"),
("G#","G#"),
("Ab","Ab"),
("A#","A#"),
("Bb","Bb")
]

rootChoices=[
(3.00,"C2"),
(3.02,"E2"),
(3.04,"D2"),
(3.05,"F2"),
(3.07,"G2"),
(3.09,"A2"),
(3.11,"B2"),
(4.00,"C3"),
(4.02,"E3"),
(4.04,"D3"),
(4.05,"F3"),
(4.07,"G3"),
(4.09,"A3"),
(4.11,"B3"),
(5.00,"C4"),
(5.02,"E4"),
(5.04,"D4"),
(5.05,"F4"),
(5.07,"G4"),
(5.09,"A4"),
(5.11,"B4")
]
moodChoices = [
    ("Happy", "Happy"),
    ("Sad", "Sad")
]
bpmChoices=[
    (60, 60),
    (120, 120),
    (180, 180)
]
instrChoices = [
    ("AcousticGuitar","Acoustic Guitar"),
    ("Piano","Piano"),
    ("Organ","Organ"),
    ("AltoSaxophone","Alto Saxophone"),
    ("Flute","Flute")
]
timSigChoices = [    
    ("2/4", "2/4"), 
    ("3/4", "3/4"),
    ("4/4", "4/4"),
    ("5/4", "5/4 (Take Five by Dave Brubeck Quartet)")
]

selectionChoices = [
    (0, "Roulette Selection"),
    (1, "Rank Based Selection")
]

crossoverChoices = [
    (0, "Single Point Crossover"),
    (1, "Two Point Crossover"),
    (2, "Multi Point Crossover"),
    (3, "Uniform Crossover")
]

# All the forms
class laymanForm(Form):
    mood = ChoiceField(choices=moodChoices, required=True, help_text="What type of music you want?", widget=RadioSelect, label="Mood")
    bpm = ChoiceField(choices=bpmChoices, required=True, help_text="Select BPM", label="BPM")
    instrument = ChoiceField(choices=instrChoices, required=True, help_text="Choose an Instrument of your choice", label="Instrument")

class virtuosoForm(Form):
    numBars = IntegerField(min_value=1, max_value=8, required=True, label="Number of Bars", initial=4)
    timeSig = ChoiceField(choices=timSigChoices, required=True, label="Select Time Signature")
    bpm = ChoiceField(choices=bpmChoices, required=True, help_text="Select BPM", label="BPM")
    keyNote = ChoiceField(choices=keyChoices, required=True, help_text="Select Key Note for you Scale", label="Key Note")
    scale = ChoiceField(choices=scaleChoices, required=True, help_text="Select Scale", label="Scale")
    rootOctave = ChoiceField(choices=rootChoices, required=True, label="Root Octave of the Scale")
    pauses =  BooleanField(label="Want to keep Pauses?", initial=False)
    numOctaves = IntegerField(min_value=1, max_value=5, required=True, label="Number of Octaves", help_text="Number of octaves you want the music to span", initial=2)
    numTracks = IntegerField(min_value=1, max_value=4, label="Number of Tracks", initial=1, required=True)
    instrument = ChoiceField(choices=instrChoices, required=True, help_text="Choose an Instrument of your choice", label="Instrument")

class expertForm(Form):
    numBars = IntegerField(min_value=1, max_value=8, required=True, label="Number of Bars", initial=4)
    timeSig = ChoiceField(choices=timSigChoices, required=True, label="Select Time Signature")
    mood = ChoiceField(choices=moodChoices, required=True, help_text="What type of music you want?", widget=RadioSelect, label="Mood")
    bpm = ChoiceField(choices=bpmChoices, required=True, help_text="Select BPM", label="BPM")
    evoStrat = ChoiceField(choices=evoChoices, required=True, label="Evolution Strategy")
    populationSize = IntegerField(min_value=2, max_value=10, required=True, label="Population Size", initial=5)
    selectionMethod = ChoiceField(choices=selectionChoices, required=True, label="Selection Method")
    crossoverMethod = ChoiceField(choices=crossoverChoices, required=True, label="Crossover Method")
    mutNum = IntegerField(max_value=100, min_value=0, label="Number of Mutations", initial=5)
    mutProb = FloatField(max_value=1.0, min_value=0.0, required=True, label="Mutation Probability", initial=0.5)
    instrument = ChoiceField(choices=instrChoices, required=True, help_text="Choose an Instrument of your choice", label="Instrument")

