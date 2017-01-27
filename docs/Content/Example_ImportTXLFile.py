####################
# Import Libraries #
####################

# Import TXLWriter, the main class for generating TXL Output
import TXLWizard.TXLWriter

# Import Pre-Defined Shapes / Structures wrapped in functions
import TXLWizard.ShapeLibrary.LabelArray

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
    'CircleArray': {
        'Columns': 6,
        'Rows': 5,
        'ArrayXOffset': 500,
        'ArrayYOffset': -500,
        'ArrayOrigin': [0.75e3, 3e3],
        'Label': 'R{j}C{i}',  # {i} and {j} will be replaced
        # by str.format() with the corresponding auto-incremented index
        'LabelXOffset': 0,
        'LabelYOffset': 100,
    }
}

########################
# Initialize TXLWriter #
########################
TXLWriter = TXLWizard.TXLWriter.TXLWriter(
    GridWidth=SampleParameters['Width'],
    GridHeight=SampleParameters['Height']
)

# Import existing TXL file
TXLWriter.ImportTXLFile('Masks/Example_Simple.txl')

# label each array element
TXLWizard.ShapeLibrary.LabelArray.GetLabelArray(
    TXLWriter,
    StructureParameters['CircleArray']['Label'],
    OriginPoint=[
        StructureParameters['CircleArray']['ArrayOrigin'][0]
        + StructureParameters['CircleArray']['LabelXOffset'],
        StructureParameters['CircleArray']['ArrayOrigin'][1]
        + StructureParameters['CircleArray']['LabelYOffset']
    ],
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
TXLWriter.GenerateFiles('Masks/Example_ImportTXLFile')
