Logic Control
=============

Faders
------

    Touch: MIDI ch 1:  Note on G#, octave 7, velocity 127
           PitchWheel on MIDI ch 1 -> 8   (-8192 -> 8176)
           MIDI ch 1:  Note off G#, octave 7

     1 | 2 | 3  | 4 | 5 | 6  | 7 | 8
    ---|---|----|---|---|----|---|---
    G# | A | A# | B | C | C# | D | D#


Buttons
-------

    MIDI ch1 Note  on E octave 0/1, velocity 127
    MIDI ch1 Note off E octave 0/1

    Notes description:

     E | F | F# | G | G# | A  | A# | B  octave 0  : first line
    ---|---|----|---|----|----|----|---
     1 | 2 | 3  | 4 | 5  | 6  | 7  | 8
    ---|---|----|---|----|----|----|---
    G# | A | A# | B | C  | C# | D  | D#  octave 1 : second line


Knob click
----------

    MIDI ch 1:  Note on  G#, octave 1, velocity 127
    MIDI ch 1:  Note off G#, octave 1

     1 | 2 | 3  | 4 | 5 | 6  | 7 | 8
    ---|---|----|---|---|----|---|---
    G# | A | A# | B | C | C# | D | D#


Knob rot
--------

MIDI ch 1, CC: 16 -> 23  value: 1->127


Other Buttons
-------------

Store: Note on/off G# octave 2, velocity 127 
Learn: Note on/off G  octave 2, velocity 127 
Edit : Note on/off F# octave 2, velocity 127 
Exit : Note on/off F  octave 2, velocity 127 

Preset <  Note on/off A# octave 2, velocity 127
Preset >  Note on/off B  octave 2, velocity 127

Top    left  :  Note on/off G    octave 6 velocity 127
Top    right :  Note on/off A    octave 6 velocity 127
Bottom left  :  Note on/off G#   octave 6 velocity 127
Bottom right :  Note on/off A#   octave 6 velocity 127





Converting note + octave to number



