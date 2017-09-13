import re

def midiNoteToNumber(note, octave):
    _notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    index = _notes.index(note)

    return ((octave+1) * 12) + index

def midiNumberToNote(number):
    _notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    index = number % 12
    note = _notes[index]
    octave = int((number-12)/12)
    #print("MIDI Note number "+str(number)+" : "+str(note)+str(octave))
    return (note,octave)


def midiNumberToFullNote(number):
    _notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    index = number % 12
    note = _notes[index]
    octave = int((number-12)/12)
    #print("MIDI Note number "+str(number)+" : "+str(note)+str(octave))
    return "{}{}".format(note,octave)


def midiFullNoteToNumber(fullNote):
    """
    Convert a note like A1, G#4 or F#-1 to a number
    """
    midiPattern = re.compile('([A-G]#?)(-?[0-9])')
    m = midiPattern.match(fullNote)

    if m:
        return int(midiNoteToNumber(str(m.group(1)), float(m.group(2))))
    
