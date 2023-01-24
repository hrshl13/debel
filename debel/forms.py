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
pauseChoices=[
    ("Yes", "Yes"),
    ("No", "No")
]


# All the forms
class laymanForm(Form):
    mood = ChoiceField(choices=moodChoices, required=True, help_text="What type of music you want?", widget=RadioSelect(), label="What is your mood?")
    mood.widget.attrs.update({'class':'radioBtn'})

    bpm = ChoiceField(choices=bpmChoices, required=True, help_text="Select BPM", label="BPM")
    bpm.widget.attrs.update({'class':'dropdown'})
    
    instrument = ChoiceField(choices=instrChoices, required=True, help_text="Choose an Instrument of your choice", label="Instrument")
    instrument.widget.attrs.update({'class':'dropdown'})

class virtuosoForm(Form):
    numBars = IntegerField(min_value=1, max_value=8, required=True, label="Number of Bars", initial=4)
    numBars.widget.attrs.update({'class':'intField'})

    timeSig = ChoiceField(choices=timSigChoices, required=True, label="Select Time Signature")
    timeSig.widget.attrs.update({'class':'dropdown'})

    bpm = ChoiceField(choices=bpmChoices, required=True, help_text="Select BPM", label="BPM")
    bpm.widget.attrs.update({'class':'dropdown'})

    keyNote = ChoiceField(choices=keyChoices, required=True, help_text="Select Key Note for you Scale", label="Key Note")
    keyNote.widget.attrs.update({'class':'dropdown'})

    scale = ChoiceField(choices=scaleChoices, required=True, help_text="Select Scale", label="Scale")
    scale.widget.attrs.update({'class':'dropdown'})

    rootOctave = ChoiceField(choices=rootChoices, required=True, label="Root Octave of the Scale")
    rootOctave.widget.attrs.update({'class':'dropdown'})

    pauses =  ChoiceField(choices=pauseChoices, label="Want to keep Pauses?",  widget=RadioSelect())
    pauses.widget.attrs.update({'class':'radioBtn'})

    numOctaves = IntegerField(min_value=1, max_value=5, required=True, label="Number of Octaves", help_text="Number of octaves you want the music to span", initial=2)
    numOctaves.widget.attrs.update({'class':'intField', 'placeholder':numOctaves.help_text})

    numTracks = IntegerField(min_value=1, max_value=4, label="Number of Tracks", initial=1, required=True)
    numTracks.widget.attrs.update({'class':'intField'})

    instrument = ChoiceField(choices=instrChoices, required=True, help_text="Choose an Instrument of your choice", label="Instrument")
    instrument.widget.attrs.update({'class':'dropdown'})

class expertForm(Form):
    numBars = IntegerField(min_value=1, max_value=8, required=True, label="Number of Bars", initial=4)
    numBars.widget.attrs.update({'class':'intField'})

    timeSig = ChoiceField(choices=timSigChoices, required=True, label="Select Time Signature")
    timeSig.widget.attrs.update({'class':'dropdown'})

    mood = ChoiceField(choices=moodChoices, required=True, help_text="What type of music you want?", widget=RadioSelect(), label="What is your mood today?")
    mood.widget.attrs.update({'class':'radioBtn'})

    bpm = ChoiceField(choices=bpmChoices, required=True, help_text="Select BPM", label="BPM")
    bpm.widget.attrs.update({'class':'dropdown'})

    evoStrat = ChoiceField(choices=evoChoices, required=True, label="Evolution Strategy")
    evoStrat.widget.attrs.update({'class':'dropdown'})

    populationSize = IntegerField(min_value=2, max_value=10, required=True, label="Population Size", initial=5)
    populationSize.widget.attrs.update({'class':'intField'})

    selectionMethod = ChoiceField(choices=selectionChoices, required=True, label="Selection Method")
    selectionMethod.widget.attrs.update({'class':'dropdown'})

    crossoverMethod = ChoiceField(choices=crossoverChoices, required=True, label="Crossover Method")
    crossoverMethod.widget.attrs.update({'class':'dropdown'})

    mutNum = IntegerField(max_value=100, min_value=0, label="Number of Mutations", initial=5)
    mutNum.widget.attrs.update({'class':'intField'})

    mutProb = FloatField(max_value=1.0, min_value=0.0, required=True, label="Mutation Probability", initial=0.5)
    mutProb.widget.attrs.update({'class':'intField'})

    instrument = ChoiceField(choices=instrChoices, required=True, help_text="Choose an Instrument of your choice", label="Instrument")
    instrument.widget.attrs.update({'class':'dropdown'})

