####################
# Import Libraries #
####################

# Import TXLWriter, the main class for generating TXL Output
import TXLWizard.TXLWriter

# Import Pre-Defined Shapes / Structures wrapped in functions
import TXLWizard.ShapeLibrary.EndpointDetectionWindows
import TXLWizard.ShapeLibrary.Markers
import TXLWizard.ShapeLibrary.Label
import TXLWizard.ShapeLibrary.CornerCube

# Import math module for calculations
import math


#################################
# Sample / Structure Parameters #
#################################

# Define all sample parameters
SampleParameters = {
    'Width': 8e3,
    'Height': 8e3,
    'Label': 'GOI Demo CornerCube',
}

# Define all structure parameters
StructureParameters = {
    'CornerCube': {
        'BridgeLength':8,
        'ParabolaFocus': 9,
        'XCutoff': 9,
        'AirGapX': 3,
        'AirGapY': 1,
        'LabelXOffset': 0,
        'LabelYOffset': 50,
        'Label': 'R{:d}C{:d}', # {:d} will be replaced
                               # by str.format() with the corresponding row / column
        'Layer': 2
    },
    'Circle': {
        'Radius': 5,
        'Layer': 3
    },
    'CornerCubeArray': {
        'Columns': 6,
        'Rows': 5,
        'ArrayXOffset': 500,
        'ArrayYOffset': -500,
        'ArrayOrigin': [0.75e3, 3e3]
    }
}


########################
# Initialize TXLWriter #
########################
TXLWriter = TXLWizard.TXLWriter.TXLWriter(
    GridWidth=SampleParameters['Width'],
    GridHeight=SampleParameters['Height']
)

#####################
# Define Structures #
#####################

## Sample Label ##

# Give the sample a nice label...
SampleLabelObject = TXLWizard.ShapeLibrary.Label.GetLabel(
    TXLWriter,
    Text=SampleParameters['Label'],
    OriginPoint=[
        0.5e3, 1. * SampleParameters['Height'] / 2. - 500
    ],
    FontSize=150,
    StrokeWidth=20,
    RoundCaps=True,# Set to False to improve e-Beam performance
    Layer=1
)
# ...and some other information
Alphabet = TXLWizard.ShapeLibrary.Label.GetLabel(
    TXLWriter,
    Text='abcdefghijklmnopqrstuvwxyz0123456789 megamega ggg ah extraaaa rischaaaar',
    OriginPoint=[
        0.5e3, 1. * SampleParameters['Height'] / 2. - 600
    ],
    FontSize=50,
    StrokeWidth=3,
    RoundCaps=True, # Set to False to improve e-Beam performance
    Layer=1
)

## Endpoint Detection ##

# Use Pre-Defined Endpoint Detection Windows
TXLWizard.ShapeLibrary.EndpointDetectionWindows.GetEndpointDetectionWindows(
    TXLWriter, Layer=1
)

## Alignment Markers ##

# Use Pre-Defined Alignment Markers
TXLWizard.ShapeLibrary.AlignmentMarkers.GetAlignmentMarkers(
    TXLWriter, Layer=1
)


## User Structure: Corner Cube ##

# Create Definition Structure for Corner Cube that will be reused
CornerCubeDefinition = TXLWizard.ShapeLibrary.CornerCube.GetCornerCube(
    TXLWriter,
    ParabolaFocus=StructureParameters['CornerCube']['ParabolaFocus'],
    XCutoff=StructureParameters['CornerCube']['XCutoff'],
    AirGapX=StructureParameters['CornerCube']['AirGapX'],
    AirGapY=StructureParameters['CornerCube']['AirGapY'],
    Layer=StructureParameters['CornerCube']['Layer']
)

# Create Definition Structure for combination of cornercube and additional circle
FullCornerCubeNoRotation = TXLWriter.AddDefinitionStructure('FullCornerCubeNoRotation')
FullCornerCubeNoRotation.AddPattern(
    'Reference',
    ReferencedStructureID=CornerCubeDefinition.ID,
    OriginPoint=[1. * StructureParameters['CornerCube']['BridgeLength'] / 2., 0]
)
FullCornerCubeNoRotation.AddPattern(
    'Circle',
    Center=[0, 0],
    Radius=StructureParameters['Circle']['Radius'],
    Layer=StructureParameters['Circle']['Layer']
)

# Create definition structure with rotation of entire referenced structure
FullCornerCube = TXLWriter.AddDefinitionStructure('FullCornerCube',
                                                  RotationAngle=45)
FullCornerCube.AddPattern(
    'Reference',
    ReferencedStructureID=FullCornerCubeNoRotation.ID,
    OriginPoint=[0, 0]
)

# Create array of the definition structure above
CornerCubeArrayFine = TXLWriter.AddContentStructure('CornerCubeArrayFine')
CornerCubeArrayFine.AddPattern(
    'Array',
    ReferencedStructureID=FullCornerCube.ID,
    OriginPoint=StructureParameters['CornerCubeArray']['ArrayOrigin'],
    PositionDelta1=[
        StructureParameters['CornerCubeArray']['ArrayXOffset'], 0
    ],
    PositionDelta2=[
        0, StructureParameters['CornerCubeArray']['ArrayYOffset']
    ],
    Repetitions1=StructureParameters['CornerCubeArray']['Columns'],
    Repetitions2=StructureParameters['CornerCubeArray']['Rows']
)


# Add Labels to each array element
for Row in range(1, StructureParameters['CornerCubeArray']['Rows'] + 1):
    for Column in range(1, StructureParameters['CornerCubeArray']['Columns'] + 1):
        RowColumnCountLabel = TXLWizard.ShapeLibrary.Label.GetLabel(
            TXLWriter,
            StructureParameters['CornerCube']['Label'].format(Row, Column),
            OriginPoint=[
                StructureParameters['CornerCubeArray']['ArrayOrigin'][0]
                + StructureParameters['CornerCubeArray']['ArrayXOffset'] * (Column - 1)
                + StructureParameters['CornerCube']['LabelXOffset'],
                StructureParameters['CornerCubeArray']['ArrayOrigin'][1]
                + StructureParameters['CornerCubeArray']['ArrayYOffset'] * (Row - 1)
                + StructureParameters['CornerCube']['LabelYOffset']],
            FontSize=16,
            StrokeWidth=3,
            RoundCaps=True,# Set to False to improve e-Beam performance
            Layer=1,
            RotationAngle=45
        )


#########################
# Generate Output Files #
#########################

# Note: The suffix (.txl, .html, .svg) will be appended automatically
TXLWriter.GenerateFiles('Masks/Example_Advanced')
