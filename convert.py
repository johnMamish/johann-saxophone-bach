#!/bin/python

# Usage:
# convert.py <input file> <output file>
# all files in humdrum.

# This program will take a score in humdrum and generate a PDF from it.  The
# generated PDF will be in the correct keys and clefs for saxophone quartet.  No
# guarantees are made about the notes all being in range.
#
#
# Future enhancements:
#    - Fix enharmonic wonkiness
#
#    - Command line flag to choose which key we are putting the output in.  This
#      would give opportunites to transpose everything into different keys
#
#    - Detection and mitigation of notes outside of saxophone range
#
#    - Handle music with key changes or clef changes

import sys
from music21 import *

keydict = {"D--": -12, "A--": -11, "E--": -10, "B--": -9, "F-": -8, "C-": -7,
           "G-": -6, "D-": -5, "A-": -4, "E-": -3, "B-": -2, "F": -1,
           "C": 0, "G": 1, "D": 2, "A": 3, "E": 4, "B": 5, "F#": 6,
           "C#": 7, "G#": 8, "D#": 9, "A#": 10, "E#": 11, "B#": 12,
           "F##": 13, "C##": 14, "G##": 15, "D##": 16, "A##": 17, "E##": 18}

# Tells how far from the key of a given part the given note is.
# For instance, if are in C major and we are looking at a C#, this will return
# C -> G -> D  -> A  -> E  -> B  ->  F# -> C# = 7 steps
#
# The same thing with an enharmonic Gb would give
# C -> F -> Bb -> Eb -> Ab -> Db              = -5 steps
#
# The note should be of type note, NOT of type pitch
def circleOfFifthsDistance(part, n):
    # Get key of part.  This is not very good, as it just grabs the first key
    # that it sees.
    if(part.measure(0) == None):
        iter = part.measure(1).getElementsByClass(key.Key)
    else:
        iter = part.measure(0).getElementsByClass(key.Key)

    k = iter[0]
    tonic = k.tonic

    #get the distance
    return keydict[n.pitch.name] - keydict[str(tonic)]

# "fixes" parts by finding enharmonic notes that may be more appropriate.
#
# It does this by evaluating each note with respect to the tonic of the piece.
# If the note is four "circle of fifths steps" in the flat direction or seven
# in the sharp direction, it is considered ok.
#
# For instance, in C major, C# is 7 "circle-of-fifths steps" from C, so it is
# considered ok.  D-, on the other hand, is 5 "circle-of-fifths steps" from C,
# so it would be transformed to a C#.
def fixUpEnharmonics(part):
    # We can't fix up enharmonics if there is not an adequate key.  Note that a
    # music21 key is not the same as a music21 key SIGNATURE, as the key
    # signature will not give us enough information about major / minor.
    # We cannot fixup enharmonics unless there is a key.
    measiter = part.getElementsByClass(stream.Measure)
    num_keys = len(measiter[0].getElementsByClass(key.Key).elements)
    if(num_keys == 0):
        print("---------no key----------\n\n")
        return

    for measure in part.getElementsByClass(stream.Measure):
        for n in measure.getElementsByClass(note.Note):
            if(circleOfFifthsDistance(part, n) < -5):
                n.pitch.getLowerEnharmonic(inPlace=True)
            elif(circleOfFifthsDistance(part, n) > 7):
                n.pitch.getHigherEnharmonic(inPlace=True)

#check number of command line arguments
if(len(sys.argv) != 3):
    print("Usage: %s <input file> <output file>\r\n\r\n", sys.argv[0]);
    sys.exit();

#load up the humdrum file
work = converter.parse(sys.argv[1]);
#print(work.metadata.title + " loaded\r\n")

# Transpose depending on part.  NB: assumes that parts come in SATB order.
#     soprano:   up 2 semitones
#     alto:      up 9 semitones
#     tenor:     up 14 semitones
#     baritone:  up 21 semitones
if(False):
    work.parts[0].transpose(2, inPlace=True);
    work.parts[1].transpose(9, inPlace=True);
    work.parts[2].transpose(14, inPlace=True);
    work.parts[3].transpose(21, inPlace=True);
else:
    work.parts[0].transpose(0, inPlace=True);
    work.parts[1].transpose(7, inPlace=True);
    work.parts[2].transpose(12, inPlace=True);
    work.parts[3].transpose(19, inPlace=True);

# Change clef depending on part
# First measure could be either 0 or 1 depending on whether there is a pickup
# or not.  Maybe there is a way to get measure by offset... but... idc.
if(work.parts[0].measure(0) == None):
    work.parts[2].measure(1).clef = clef.TrebleClef();
    work.parts[3].measure(1).clef = clef.TrebleClef();
else:
    work.parts[2].measure(0).clef = clef.TrebleClef();
    work.parts[3].measure(0).clef = clef.TrebleClef();

for part in work.parts:
    fixUpEnharmonics(part)

#generate PDF
#work.show()
lpc = lily.translate.LilypondConverter()
lpc.loadObjectFromScore(work)
lpc.createPDF(sys.argv[2].replace(".pdf", ""))
