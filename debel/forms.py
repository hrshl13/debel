from django.forms import Form, ChoiceField
from django.forms.widgets import RadioSelect


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

class laymanForm(Form):
    mood = ChoiceField(choices=moodChoices, required=True, help_text="What is your mood?: ", widget=RadioSelect, label="Mood: ")
    bpm = ChoiceField(choices=bpmChoices, required=True, help_text="Select BPM", label="BPM")
    instrument = ChoiceField(choices=instrChoices, required=True, help_text="Choose an Instrument of your choice", label="Instrument")


