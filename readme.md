
Overview
------------
This repository contains code to automatically arrange bach chorales in humdrum
format (*.krn) for saxophone quartet.

Please note that if you don't know anything about programming and you just want
some damn chorales, they can be downloaded at (link coming soon, project under
construction).

The key directories and bits of code are as follows:
    1. bach-371-chorales
       A subrepository containing 371 Bach chorales in the humdrum format.
       Thanks to Craig Sapp from Stanford for putting these together.

    2. johann-saxophone-bach.py
       A python script that transposes a single humdrum file from bach chorale
       arrangement into saxophone quartet arrangement.

       If you dig into the makefile and edit the command line options passed to
       the script, there are a few interesting and possibly useful ways to
       change the output.  For instance, you can have an arrangement for AATB
       generated instead of SATB, or you can alter the final key (as long as it
       doesn't violate the highest and lowest pitches for saxophone).

       In the future, I might rework this to work for arbitrary ensembles.

    3. Makefile
       The makefile runs the above script on all of the humdrum files in the
       bach-371-chorales repository and generates pdfs as output in the "build"
       directory.



Requirements
------------
As this requires make, it's probably not worth the effort to get it to run
windows.  You need linux and a basic familiarity with the command line.

You will need python > 2.7.3 or > 3.3.  Instructions for installing python can
be found [here](https://wiki.python.org/moin/BeginnersGuide/Download)

You will need the music21 python library.  Installation instructions can be
found at [music21's website](http://web.mit.edu/music21/doc/installing/install.html#install)
(thanks MIT).

After that, just run make in the top-level directory.
