# Import TXLWriter, the main class for generating TXL Output
import TXLWizard.TXLWriter

# Import Pre-Defined Shapes / Structures wrapped in functions
import TXLWizard.ShapeLibrary.Label

# Initialize TXLWriter
TXLWriter = TXLWizard.TXLWriter.TXLWriter()

# Give the sample a nice label
SampleLabelObject = TXLWizard.ShapeLibrary.Label.GetLabel(
    TXLWriter,
    Text='This is my text',
    OriginPoint=[-310, 240],
    FontSize=50,
    StrokeWidth=5,
    RoundCaps=True,  # Set to False to improve e-Beam performance
    Layer=1
)

# Create Content Structure for Circle with ID `MyCircle`
CircleStructure = TXLWriter.AddContentStructure('MyCircle')

# Add a `Pattern` of type `Circle`
CircleStructure.AddPattern(
    'Circle',
    Center=[0, 0],
    Radius=150,
    Layer=2
)

# Generate Output Files
# Note: The suffix (.txl, .html, .svg) will be appended automatically
TXLWriter.GenerateFiles('Masks/Example_Introduction')

