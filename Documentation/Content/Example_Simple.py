####################
# Import Libraries #
####################

# Import TXLWriter, the main class for generating TXL Output
import TXLWizard.TXLWriter

# Import Pre-Defined Shapes / Structures wrapped in functions
import TXLWizard.ShapeLibrary.EndpointDetectionWindows
import TXLWizard.ShapeLibrary.Label

# Import math module for calculations
import math


#################################
# Sample / Structure Parameters #
#################################

# Define all sample parameters
SampleParameters = {
    'Width': 8e3,
    'Height': 8e3,
    'Label': 'Simple Demo',
}

# Define all structure parameters
StructureParameters = {
    'Circle': {
        'Radius': 50,
        'Layer': 3
    },
    'CircleArray': {
        'Columns': 6,
        'Rows': 5,
        'ArrayXOffset': 500,
        'ArrayYOffset': -500,
        'ArrayOrigin': [0.75e3, 3e3],
        'Label': 'R{:d}C{:d}',
    }
}


########################
# Initialize TXLWriter #
########################
TXLWriter = TXLWizard.TXLWriter.TXLWriter(
    Width=SampleParameters['Width'],
    Height=SampleParameters['Height']
)

#####################
# Define Structures #
#####################

## Sample Label ##

# Give the sample a nice label
SampleLabelObject = TXLWizard.ShapeLibrary.Label.GetLabel(
    TXLWriter,
    SampleParameters['Label'],
    OriginPoint=[0.5e3, 1. * SampleParameters['Height'] / 2. - 500],
    FontSize=150,
    StrokeWidth=20,
    RoundCaps=True,
    Layer=1
)


## Endpoint Detection ##

# Use Pre-Defined Endpoint Detection Windows
TXLWizard.ShapeLibrary.EndpointDetectionWindows.GetEndpointDetectionWindows(
    TXLWriter, Layer=1)

## User Structure: Circle ##

# Create Definition Structure for Circle that will be reused
CircleStructure = TXLWriter.AddDefinitionStructure('Circle')
CircleStructure.AddPattern('Circle',
    Center=[0, 0],
    Radius=StructureParameters['Circle']['Radius'],
    Layer=StructureParameters['Circle']['Layer']

)

# Create array of the definition structure above
CircleArray = TXLWriter.AddContentStructure('CircleArray')
CircleArray.AddPattern('Array',
    ReferencedStructureID=CircleStructure.ID,
    OriginPoint=StructureParameters['CircleArray']['ArrayOrigin'],
    PositionDelta1=[
        StructureParameters['CircleArray']['ArrayXOffset'], 0
    ],
    PositionDelta2=[
        0, StructureParameters['CircleArray']['ArrayYOffset']
    ],
    Repetitions1=StructureParameters['CircleArray']['Columns'],
    Repetitions2=StructureParameters['CircleArray']['Rows']
)



#########################
# Generate Output Files #
#########################

# Note: The suffix (.txl, .html, .svg) will be appended automatically
TXLWriter.GenerateFiles('Masks/Example_Simple')

