###########################################
# Import Libraries / Initialize TXLWriter #
###########################################

# Import TXLWriter, the main class for generating TXL Output
import TXLWizard.TXLWriter

# Import Pre-Defined Shapes / Structures wrapped in functions
import TXLWizard.ShapeLibrary.Label

# Initialize TXLWriter
TXLWriter = TXLWizard.TXLWriter.TXLWriter()

#####################
# Define Structures #
#####################

## Sample Label ##

# Give the sample a nice label
SampleLabelObject = TXLWizard.ShapeLibrary.Label.GetLabel(
    TXLWriter,
    'This is my text',
    OriginPoint=[
        0.5e3, 3e3
    ],
    FontSize=150,
    StrokeWidth=20,
    RoundCaps=True,  # Set to False to improve e-Beam performance
    Layer=1
)

## User Structure: Circle ##

# Create Content Structure for Circle
CircleStructure = TXLWriter.AddContentStructure('Circle')

# Add a `Pattern` of type `Circle`
CircleStructure.AddPattern('Circle',
    Center=[20, 10],
    Radius=5,
    Layer=2

)

#########################
# Generate Output Files #
#########################

# Note: The suffix (.txl, .html, .svg) will be appended automatically
TXLWriter.GenerateFiles('Masks/Example_Introduction')
