def midiNoteToNumber(note, octave):
    _notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    index = _notes.index(note)

    return ((octave+1) * 12) + index

def midiNumberToNote(number):
    _notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    index = number % 12
    note = _notes[index]
    octave = int((number-12)/12)
    print("MIDI Note number "+str(number)+" : "+str(note)+str(octave))
    return (note,octave)

