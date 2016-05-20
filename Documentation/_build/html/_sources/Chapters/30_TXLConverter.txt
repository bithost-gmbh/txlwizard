.. _sec-TXLConverter:

TXLConverter
============

For existing TXL files, there is a command line interface script that converts them to SVG / HTML files.

Usage
-----
The usage is very simple. Simply run the python script `TXLWizard/TXLConverterCLI.py`.
The command line interface will allow you to change the configuration as you wish. Furthermore, the configuration is saved
and restored for a subsequent run.



Code
####
To use the `TXLConverter` from the command line type

.. code-block:: bash

    python TXLWizard/Tools/TXLConverterCLI.py

Or if you want to call it in your own script do

.. code-block:: python

    import TXLWizard.TXLConverter
    TXLConverterCLI = TXLWizard.TXLConverter.TXLConverterCLI()

The resulting command line interface looks as follows:
::

    ### TXL Converter v1.6 ###
    Converts TXL Files to SVG/HTML
    written by Esteban Marin (estebanmarin@gmx.ch)


    Full TXL File / Folder Path
    If the path is a folder, you can enter the filename separately.
    [/home/john.mega/masks]: /Users/esteban/Desktop/masks2/tmpd/EM160225_GOI_CornerCube_Microbridge.txl

    SampleWidth in um
    used to draw coordinate system
    [1500]:

    SampleHeight in um
    used to draw coordinate system
    [1500]:

    Layers to process
    comma-separated, e.g. 1,4,5. Type -1 for all layers.
    [-1]:

    Do Conversion (y/n)? [y]

    Files written:
    /Users/esteban/Desktop/masks2/tmpd/EM160225_GOI_CornerCube_Microbridge.html
    /Users/esteban/Desktop/masks2/tmpd/EM160225_GOI_CornerCube_Microbridge.svg

    Done
