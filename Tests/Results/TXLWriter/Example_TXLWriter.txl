LETXTLIB 1.0.0
UNIT MICRON
RESOLVE 0.0001
BEGLIB


! ### Definitions Start ###
STRUCT MyDefinition
LAYER 3
C 20.0000 0.0000,0.0000 ENDC
ENDSTRUCT



! ### Definitions End ###



! ### Content Structures Start ###
STRUCT MySuperCircle
SREF MyDefinition 20.0000,50.0000 
ENDSTRUCT



! ### Content Structures End ###
ENDLIB
