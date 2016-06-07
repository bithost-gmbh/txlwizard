LETXTLIB 1.0.0
UNIT MICRON
RESOLVE 0.0001
BEGLIB


! ### Definitions Start ###
STRUCT MyCircleID
LAYER 1
C 50.0000 0.0000,0.0000 ENDC
ENDSTRUCT



! ### Definitions End ###



! ### Content Structures Start ###
STRUCT MyCircleArray
AREF MyCircleID (40.0000,60.0000) 10 (100.0000,0.0000) 20 (0.0000,200.0000)
ENDSTRUCT



! ### Content Structures End ###
ENDLIB
