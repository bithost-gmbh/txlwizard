Introduction
============
This document describes the usage and technical reference of the python program `TXLWizard`
written by Esteban Marin (estebanmarin@gmx.ch).

What does it do?
----------------
The `TXLWizard` provides routines for generating TXL files (.txl) for
the preparation of E-Beam lithography masks using python code. The TXL files can be processed with BEAMER.
See the following links:

* http://genisys-gmbh.com/web/products/beamer.html
* http://cad035.psi.ch/LB_index.html
* http://cad035.psi.ch/LBDoc/BEAMER_Manual.pdf

The generated TXL files are also converted to HTML / SVG for presentation in any modern browser or
vector graphics application.

Moreover, a command line interface `TXLConverter` provides conversion of existing TXL files to HTML / SVG
(See Section :ref:`sec-TXLConverter`).


Installation
------------
The "TXLWizard" is written in python and will run in Python version 2.7+ and 3.1+.

| In order to use it, the `TXLWizard` package must be available as
| a python package, i.e. either it must be copied to
|    :file:`Path_to_my_python_installation/site-packages/`
| or to the path where your script is located.

| Alternatively, you can also prepend the following command to your python script:
|   ``sys.path.append('path to the folder containing TXLWizard')``


Glossary
--------
The following terms are used throughout this manual:

`Structure`
^^^^^^^^^^^
Refers to an object containing one or more `Pattern` objects.
A `Structure` corresponds to the `STRUCT` command in TXL files.

`Pattern`
^^^^^^^^^
Refers to a pattern such as a circle, a polygon, an ellipse, a path, etc.
The following patterns with the corresponding TXL command in brackets are supported:

* `Circle` (`C`)
* `Ellipse` (`ELP`)
* `Polygon` (`B`)
* `Polyline` (`P`)
* `Reference` (`SREF`)
* `Array` (`AREF`)

For more information, supported parameters, etc., see Section :ref:`PythonModuleReferencePatterns`.

`Attribute`
^^^^^^^^^^^
Refers to an property of a `Pattern` determining the visual appearance of the `Pattern`.
The following attributes with the corresponding TXL command in brackets are supported:

* `Layer` (`LAYER`)
* `DataType` (`DATATYPE`)
* `RotationAngle` (`ANGLE`)
* `StrokeWidth` (`WIDTH`)
* `ScaleFactor` (`MAG`)

Please note that the `TXLWizard` strictly implements the specification of the TXL format.
This implies some peculiarities, such as

* `Attribute` commands preceed the corresponding `Pattern` in a `Structure` and are valid for all patterns that follow
  unless the attribute value is changed. Therefore, when adding a `Pattern` to a `Structure` with certain attributes,
  the attributes are valid for any subsequently added pattern, unless a different attribute value is specified.
* `Attribute` commands are valid for all patterns, except for `Reference` (`SREF`) and `Array` (`AREF`).
  Therefore the attributes of a pattern can only be specified in the structure where the pattern is added / defined.


Example SVG Output
------------------
An example output can be seen here:

.. figure:: /Content/Mask_Example.png

    Example SVG output for a mask

