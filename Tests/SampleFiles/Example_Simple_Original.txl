LETXTLIB 1.0.0
UNIT MICRON
RESOLVE 0.0001
BEGLIB


! ### Definitions Start ###
STRUCT AutoID_0
LAYER 1
WIDTH 20.0000
PR 75.0000,131.2500 75.0000,150.0000 ENDP
PR 75.0000,150.0000 0.0000,150.0000 ENDP
PR 0.0000,150.0000 0.0000,75.0000 ENDP
PR 0.0000,75.0000 75.0000,75.0000 ENDP
PR 75.0000,75.0000 75.0000,0.0000 ENDP
PR 75.0000,0.0000 0.0000,0.0000 ENDP
PR 0.0000,0.0000 0.0000,18.7500 ENDP
PR 170.0000,150.0000 170.0000,0.0000 ENDP
PR 265.0000,0.0000 265.0000,150.0000 ENDP
PR 265.0000,150.0000 302.5000,75.0000 ENDP
PR 302.5000,75.0000 340.0000,150.0000 ENDP
PR 340.0000,150.0000 340.0000,0.0000 ENDP
PR 397.5000,0.0000 397.5000,150.0000 ENDP
PR 397.5000,150.0000 472.5000,150.0000 ENDP
PR 472.5000,150.0000 472.5000,75.0000 ENDP
PR 472.5000,75.0000 397.5000,75.0000 ENDP
B 397.5000,75.0000 472.5000,75.0000 472.5000,150.0000 397.5000,150.0000 ENDB
PR 530.0000,150.0000 530.0000,0.0000 ENDP
PR 530.0000,0.0000 605.0000,0.0000 ENDP
PR 737.5000,150.0000 662.5000,150.0000 ENDP
PR 662.5000,150.0000 662.5000,0.0000 ENDP
PR 662.5000,0.0000 737.5000,0.0000 ENDP
PR 662.5000,75.0000 737.5000,75.0000 ENDP
PR 1002.5000,150.0000 1002.5000,0.0000 ENDP
PR 1002.5000,0.0000 927.5000,0.0000 ENDP
PR 927.5000,0.0000 927.5000,75.0000 ENDP
PR 927.5000,75.0000 1002.5000,75.0000 ENDP
B 927.5000,0.0000 927.5000,75.0000 1002.5000,75.0000 1002.5000,0.0000 ENDB
PR 1135.0000,150.0000 1060.0000,150.0000 ENDP
PR 1060.0000,150.0000 1060.0000,0.0000 ENDP
PR 1060.0000,0.0000 1135.0000,0.0000 ENDP
PR 1060.0000,75.0000 1135.0000,75.0000 ENDP
PR 1192.5000,0.0000 1192.5000,150.0000 ENDP
PR 1192.5000,150.0000 1230.0000,75.0000 ENDP
PR 1230.0000,75.0000 1267.5000,150.0000 ENDP
PR 1267.5000,150.0000 1267.5000,0.0000 ENDP
PR 1325.0000,0.0000 1325.0000,150.0000 ENDP
PR 1325.0000,150.0000 1400.0000,150.0000 ENDP
PR 1400.0000,150.0000 1400.0000,0.0000 ENDP
PR 1400.0000,0.0000 1325.0000,0.0000 ENDP
PR 1325.0000,0.0000 1325.0000,75.0000 ENDP
B 1325.0000,0.0000 1325.0000,150.0000 1400.0000,150.0000 1400.0000,0.0000 ENDB
ENDSTRUCT

STRUCT EndpointDetectionWindows
LAYER 1
B -500.0000,-500.0000 500.0000,-500.0000 500.0000,500.0000 -500.0000,500.0000 ENDB
B -1875.0000,-375.0000 -1125.0000,-375.0000 -1125.0000,375.0000 -1875.0000,375.0000 ENDB
B -375.0000,1125.0000 375.0000,1125.0000 375.0000,1875.0000 -375.0000,1875.0000 ENDB
B 1125.0000,-375.0000 1875.0000,-375.0000 1875.0000,375.0000 1125.0000,375.0000 ENDB
B -375.0000,-1875.0000 375.0000,-1875.0000 375.0000,-1125.0000 -375.0000,-1125.0000 ENDB
ENDSTRUCT

STRUCT MyCircleID
LAYER 3
C 50.0000 0.0000,0.0000 ENDC
ENDSTRUCT



! ### Definitions End ###



! ### Content Structures Start ###
STRUCT AutoID_0Content
LAYER 1
ANGLE 0.0000
SREF AutoID_0 500.0000,3500.0000 
ENDSTRUCT

STRUCT EndpointDetectionWindowsContent
SREF EndpointDetectionWindows 0.0000,0.0000 
ENDSTRUCT

STRUCT MyCircleArray
AREF MyCircleID (750.0000,3000.0000) 6 (500.0000,0.0000) 5 (0.0000,-500.0000)
ENDSTRUCT



! ### Content Structures End ###
ENDLIB
