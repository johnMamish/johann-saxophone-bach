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
#    - Command line flag to choose which key we are putting the output in.  This
#      would give opportunites to transpose everything into different keys
#
#    - Detection and mitigation of notes outside of saxophone range

import sys
from music21 import *

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
work.parts[0].transpose(2, inPlace=True);
work.parts[1].transpose(9, inPlace=True);
work.parts[2].transpose(14, inPlace=True);
work.parts[3].transpose(21, inPlace=True);

# Change clef depending on part
# First measure could be either 0 or 1 depending on whether there is a pickup
# or not.  Maybe there is a way to get measure by offset... but... idc.
if(work.parts[0].measure(0) == None):
    work.parts[2].measure(1).clef = clef.TrebleClef();
    work.parts[3].measure(1).clef = clef.TrebleClef();
else:
    work.parts[2].measure(0).clef = clef.TrebleClef();
    work.parts[3].measure(0).clef = clef.TrebleClef();

#generate PDF
#work.show()
lpc = lily.translate.LilypondConverter()
lpc.loadObjectFromScore(work)
lpc.createPDF(sys.argv[2].replace(".pdf", ""))
