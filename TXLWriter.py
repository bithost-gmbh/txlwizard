'''
Controller class for generating TXL / SVG / HTML output.\n
Here we can add structures (definitions and content) which will be rendered in the output.
'''

from Patterns import Definitions
from Patterns import Structure
import TXLConverter
import os.path


class TXLWriter(object):
    '''
    Controller class for generating TXL / SVG / HTML output.\n
    Here we can add structures (definitions and content) which will be rendered in the output.\n
    Optionally, a coordinate system grid is drawn.

    Parameters
    ----------
    ShowGrid : bool, optional
        Show the coordinate system grid or not.\n
        Defaults to True
    GridWidth : int, optional
        Full width of the coordinate system grid in um.\n
        Defaults to 800
    GridHeight : int, optional
        Full height of the coordinate system grid in um.\n
        Defaults to 800
    GridSpacing : int, optional
        Coordinate Sytem Grid Spacing in um.\n
        Defaults to 100
    SubGridSpacing : int, optional
        Coordinate System Sub-Grid Spacing in um.\n
        Defaults to 10
    Precision : int, optional
        Number of digits for float to str conversion / Resolution of TXL file.\n
        Defaults to 4

    Examples
    --------

    IGNORE:

        >>> import sys
        >>> import os.path
        >>> sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../'))

    IGNORE

    Import required Modules

    >>> import TXLWizard.TXLWriter

    Initialize TXLWriter

    >>> TXLWriter = TXLWizard.TXLWriter.TXLWriter(
    ...    ShowGrid=True, GridWidth=800, GridHeight=800
    ... )

    Add a definition structure and add a pattern of type `Circle`

    >>> MyDefinitionStructure = TXLWriter.AddDefinitionStructure('MyDefinition')
    >>> MyDefinitionStructure.AddPattern('Circle', Center=[0,0], Radius=20, Layer=3) #doctest: +ELLIPSIS
    <TXLWizard.Patterns.Circle.Circle object at 0x...>

    Add a content structure with a pattern `Reference` to reuse the definition structure.

    >>> MyContentStructure = TXLWriter.AddContentStructure('MySuperCircle')
    >>> MyContentStructure.AddPattern(
    ...    'Reference',
    ...    ReferencedStructureID=MyDefinitionStructure.ID,
    ...    OriginPoint=[20,50]
    ... ) #doctest: +ELLIPSIS
    <TXLWizard.Patterns.Reference.Reference object at 0x...>

    Generate the Output files with name `Example_TXLWriter.(txl|html|svg)` to the folder `Tests/Results`

    >>> TXLWriter.GenerateFiles('Tests/Results/TXLWriter/Example_TXLWriter')
    '''

    def __init__(self, **kwargs):

        #: float: current software version
        self._Version = 1.7

        #: :class:`TXLWizard.Patterns.Definitions.Definitions`: container for definition structures
        self._Definitions = Definitions.Definitions()

        #: bool: Show the coordinate system grid or not
        self._ShowGrid = True

        #: int: Full width of the coordinate system grid in um
        self._GridWidth = 800
        #: int: Full height of the coordinate system grid in um
        self._GridHeight = 800

        #: int: Coordinate Sytem Grid Spacing in um.
        self._GridSpacing = 100

        #: int: Coordinate Sytem Sub Grid Spacing in um.
        self._SubGridSpacing = 10

        #: int: Width of the SVG Image in pixels
        self._SVGWidth = 800

        #: int: Height of the SVG Image in pixels
        self._SVGHeight = 800

        #: int: number of digits for float to str conversion / Resolution of TXL file
        self._Precision = 4

        #: int: incrementing number for automatically created indices
        self._AutoIndexIncrement = 0

        #: dict: dictionary of all content structures
        self._ContentStructures = {}

        #: list of str: list of indices of content structures, needed for correct order
        self._ContentStructuresIndexList = []

        #: dict: dictionary of all helper structures
        self._HelperStructures = {}

        #: list of str: list of indices of helper structures, needed for correct order
        self._HelperStructuresIndexList = []

        for i in ['GridWidth', 'GridHeight', 'GridSpacing', 'SubGridSpacing', 'ShowGrid', 'Precision']:
            if i in kwargs:
                setattr(self, '_' + i, kwargs[i])

        if self._ShowGrid:
            self._DrawGrid()

    def _DrawGrid(self):
        '''
        Draws the coordinate system grids (grid and sub-grid)
        '''
        LineWidth = 10 * 1. / 2.

        CoordinateXAxis = self._AddHelperStructure('CoordinateXAxis')
        CoordinateXAxis.AddPattern('Polyline', Points=[
            [-self._GridWidth / 2, 0],
            [self._GridWidth / 2, 0]
        ], StrokeWidth=LineWidth)

        CoordinateYAxis = self._AddHelperStructure('CoordinateYAxis')
        CoordinateYAxis.AddPattern('Polyline', Points=[
            [0, -self._GridHeight / 2],
            [0, self._GridHeight / 2]
        ], StrokeWidth=LineWidth)

        Grids = {}

        for GridName in ['Grid', 'SubGrid']:
            Grid = self._AddHelperStructure(GridName)
            Grids[GridName] = Grid
            GridSpacing = self.__getattribute__('_' + GridName + 'Spacing')
            if GridName == 'SubGrid':
                LineWidth = 1. / 2.
            for i in range(0, int(round(self._GridWidth / GridSpacing / 2))):
                for j in [-i * GridSpacing, i * GridSpacing]:
                    Grid.AddPattern('Polyline', Points=[
                        [1. * j, -self._GridHeight / 2.],
                        [1. * j, self._GridHeight / 2.]
                    ], StrokeWidth=LineWidth)
            for i in range(0, int(round(self._GridHeight / GridSpacing / 2))):
                for j in [-i * GridSpacing, i * GridSpacing]:
                    Grid.AddPattern('Polyline', Points=[
                        [-self._GridWidth / 2., 1. * j],
                        [self._GridWidth / 2., 1. * j]
                    ], StrokeWidth=LineWidth)

    def AddDefinitionStructure(self, ID, **kwargs):
        '''
        Add definition structure. A definition structure can be referenced by a content structure.\n
        A structure corresponds to the "STRUCT" command in the TXL file format.

        Parameters
        ----------
        ID: str
            Unique identification of the structure. Must be used when referencing to this structure.
        kwargs: dict
            Keyword arguments passed to the structure constructor. See :class:`TXLWizard.Patterns.Structure.Structure`

        Returns
        -------
        :class:`TXLWizard.Patterns.Structure.Structure` structure instance
        '''
        if ID in self._Definitions.Structures:
            print('Warning! The structure "' + ID + '" already exists and will be overwritten!')

        kwargs['TXLWriter'] = self

        StructureObject = Structure.Structure(ID, **kwargs)
        self._Definitions.AddStructure(ID, StructureObject)
        return StructureObject

    def AddContentStructure(self, ID, **kwargs):
        '''
        Add content structure. A content structure can hold patterns that will render in the output.\n
        A structure corresponds to the "STRUCT" command in the TXL file format.

        Parameters
        ----------
        ID: str
            Unique identification of the structure. Must be used when referencing to this structure.
        kwargs: dict
            Keyword arguments passed to the structure constructor. See :class:`TXLWizard.Patterns.Structure.Structure`

        Returns
        -------
        :class:`TXLWizard.Patterns.Structure.Structure` structure instance
        '''
        if ID in self._ContentStructures:
            print('Warning! The structure "' + ID + '" already exists and will be overwritten!')

        kwargs['TXLWriter'] = self
        StructureObject = Structure.Structure(ID, **kwargs)
        self._ContentStructures[ID] = StructureObject
        self._ContentStructuresIndexList.append(ID)
        return self._ContentStructures[ID]

    def _AddHelperStructure(self, ID, **kwargs):
        '''
        Add helper structure. Helper structures are only visible in the HTML / SVG Output.\n
        A structure corresponds to the "STRUCT" command in the TXL file format.

        Parameters
        ----------
        ID: str
            Unique identification of the structure. Must be used when referencing to this structure.
        kwargs: dict
            keyword arguments passed to the structure constructor

        Returns
        -------
        :class:`TXLWizard.Patterns.Structure.Structure` structure instance
        '''
        if ID in self._HelperStructures:
            print('Warning! The structure "' + ID + '" already exists and will be overwritten!')

        kwargs['TXLWriter'] = self
        StructureObject = Structure.Structure(ID, **kwargs)
        self._HelperStructures[ID] = StructureObject
        self._HelperStructuresIndexList.append(ID)
        return self._HelperStructures[ID]

    def ImportTXLFile(self, Filename, LayersToProcess=[]):
        '''
        Import an existing TXL file for further processing.\n
        The content structures can be accessed with `self._ContentStructures` (read-only!).\n
        The order of the content structures is stored in `self._ContentStructuresIndexList` (read-only!).\n
        The definition structures are stored in `self._Definitions.Structures`

        Parameters
        ----------
        Filename : str
            Path / Filename of the .txl file to be imported
        LayersToProcess : list of int, optional
            if given, only layers in this list are processed / shown.\n
            Defaults to []

        Examples
        --------

        Import required modules

        >>> import TXLWizard.TXLWriter
        >>> import TXLWizard.ShapeLibrary.Label

        Initialize TXLWriter

        >>> TXLWriter = TXLWizard.TXLWriter.TXLWriter()

        import TXL file `myPath/mask_orig.txl`

        >>> TXLWriter.ImportTXLFile('Tests/SampleFiles/Example_Simple_Original.txl', LayersToProcess=[1,3,4])

        Get an existing structure and add a pattern to it

        >>> MyStructure = TXLWriter._ContentStructures['MyCircleArray']
        >>> MyStructure.AddPattern(
        ...     'Circle',
        ...     Center=[-100, 0],
        ...     Radius=50,
        ...     Layer=1
        ... ) #doctest: +ELLIPSIS
        <TXLWizard.Patterns.Circle.Circle object at 0x...>

        Add a label

        >>> SampleLabelObject = TXLWizard.ShapeLibrary.Label.GetLabel(
        ...     TXLWriter,
        ...     Text='This is my text',
        ...     OriginPoint=[
        ...         -200, 300
        ...     ],
        ...     FontSize=150,
        ...     StrokeWidth=20
        ... )

        Generate the Output files with name `ExampleSimple_Modified.(txl|html|svg)` to the folder `Tests/Results`

        >>> TXLWriter.GenerateFiles('Tests/Results/TXLWriter/Example_Simple_Modified')

        '''
        TXLConverterObject = TXLConverter.TXLConverter(Filename, LayersToProcess=LayersToProcess, TXLWriter=self)
        TXLConverterObject.ParseTXLFile()

    def _GetAutoStructureID(self, Prefix='AutoID'):
        '''
        Generates a unique structure ID.

        Parameters
        ----------
        Prefix: str, optional
            Prefix of the ID.\n
            Defaults to 'AutoID'.

        Returns
        -------
        str
            generated ID

        '''

        ID = Prefix + '_{:d}'.format(self._AutoIndexIncrement)
        self._AutoIndexIncrement += 1
        return ID

    def _GetFloatFormatString(self, ID=''):
        '''
        Returns a string for formatting a `float`, e.g. `{ID:1.3f}`.
        The number of digits is specified by `self._Precision`

        Parameters
        ----------
        ID: str, optional
            Optional ID for the formatting option.\n
            Defaults to ''

        Returns
        -------
        str:
            string for use with the `str.format()` function

        '''

        if self._Precision > 0:
            FloatFormatString = '{' + str(ID) + ':1.' + str(self._Precision) + 'f}'
        else:
            FloatFormatString = '{' + str(ID) + ':1.0f}'

        return FloatFormatString

    def GenerateFiles(self, Filename, TXL=True, SVG=True, HTML=True, TargetFolder=None):
        '''
        Generate the output files (.txl, .svg, .html).

        Parameters
        ----------
        Filename: str
            Path / Filename without extension.
            The corresponding path will be created if it does not exist
        TXL: bool, optional
            Enable TXL Output.\n
            Defaults to True
        SVG: bool, optional
            Enable SVG Output.\n
            Defaults to True
        HTML: bool, optional
            Enable HTML Output. If set to `True`,
            also `SVG` needs to be set to `True`\n
            Defaults to True
        TargetFolder: str, optional
            If given, the generated files are stored in the folder specified.\n
            If not given, the generated files are stored in the path specified in `Filename`\n
            Defaults to None.
        '''
        Path = os.path.dirname(Filename)
        if TargetFolder != None:
            Path = TargetFolder
            Filename = Path.rstrip('/')+'/'+os.path.basename(Filename)

        if len(Path) and not os.path.exists(Path):
            os.makedirs(Path)

        if TXL:
            self._GenerateTXLFile(Filename)

        if SVG:
            self._GenerateSVGFile(Filename)

        if HTML:
            self._GenerateHTMLFile(Filename)

    def _GenerateTXLFile(self, Filename):
        '''
        Generate the TXL file.

        Parameters
        ----------
        Filename: str
            Path / Filename without extension.
        '''
        f = open(Filename + '.txl', 'w')
        f.write('LETXTLIB 1.0.0' + '\n')
        f.write('UNIT MICRON' + '\n')
        f.write(('RESOLVE ' + self._GetFloatFormatString()).format(10 ** (-1 * self._Precision)) + '\n')
        f.write('BEGLIB' + '\n')
        f.write('\n\n' + '! ### Definitions Start ###' + '\n')
        f.write(self._Definitions.GetTXLOutput())
        f.write('\n\n' + '! ### Definitions End ###' + '\n\n')
        f.write('\n\n' + '! ### Content Structures Start ###' + '\n')
        for i in self._ContentStructuresIndexList:
            if self._ContentStructures[i].TXLOutput:
                f.write(self._ContentStructures[i].GetTXLOutput())
        f.write('\n\n' + '! ### Content Structures End ###' + '\n')

        f.write('ENDLIB' + '\n')
        f.close()

    def _GenerateSVGFile(self, Filename):
        '''
        Generate the TXL file.

        Parameters
        ----------
        Filename: str
            Path / Filename without extension.
        '''
        # See https://developer.mozilla.org/en-US/docs/Web/SVG

        f = open(Filename + '.svg', 'w')
        f.write('<svg version="1.1" baseProfile="full" width="800" height="800" ' +
                'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" ' +
                'id="SVGImage" viewBox="{:d} {:d} {:d} {:d}">'.format(int(-self._GridWidth / 2),
                                                                      int(-self._GridHeight / 2), int(self._GridWidth),
                                                                      int(self._GridHeight)) + '\n')
        f.write('''
            <style type="text/css">
              <![CDATA[
                #HelperStructures{}
                #HelperStructures .Pattern{opacity:0.8}
                #CoordinateXAxis .Pattern{stroke:#000}
                #CoordinateYAxis .Pattern{stroke:#000}
                #HelperStructures #Grid .Pattern{opacity:0.1;stroke:#000}
                #HelperStructures #SubGrid .Pattern{opacity:0.1;stroke:#188487}
                .Pattern{stroke-width:0px;}
                .Layer0 .Pattern{fill:#467821;stroke:#467821;}
                .Layer1 .Pattern{fill:#348ABD;stroke:#348ABD;}
                .Layer2 .Pattern{fill:#E24A33;stroke:#E24A33;}
                .Layer3 .Pattern{fill:#A60628;stroke:#A60628;}
                .Layer4 .Pattern{fill:#CF4457;stroke:#CF4457;}
                .Pattern{opacity:0.6}
                /*.Pattern:hover, .Object:hover .Pattern{opacity:0.8}*/
              ]]>
            </style>
        ''')
        f.write(self._Definitions.GetSVGOutput())
        f.write('<g transform="translate({:1.2f},{:1.2f}),matrix(1,0,0,-1,0,0)">'.format(1. * self._SVGWidth / 2.,
                                                                                         1. * self._SVGHeight / 2.) + '\n')
        f.write('<g id="HelperStructures">' + '\n')
        for i in self._HelperStructuresIndexList:
            f.write(self._HelperStructures[i].GetSVGOutput())
        f.write('</g>')
        f.write('<g id="ContentStructures">' + '\n')
        for i in self._ContentStructuresIndexList:
            f.write(self._ContentStructures[i].GetSVGOutput())
        f.write('</g>')
        f.write('</g>')
        f.write('</svg>')
        f.close()

    def _GenerateHTMLFile(self, Filename):
        '''
        Generate the TXL file.

        Parameters
        ----------
        Filename: str
            Path / Filename without extension.
        '''
        f = open(Filename + '.svg', 'r')
        SVGData = f.read()
        f.close()

        f = open(Filename + '.html', 'w')
        f.write('<html>')
        f.write('''
        <head>
            <style>
                body{margin:0px;padding:0px;}
                #SVGImage {box-sizing:border-box;-moz-box-sizing:border-box;-ms-box-sizing:border-box;}
            </style>
        </head>
        ''')
        PanZoom = open(os.path.dirname(__file__) + '/Helpers/svg-pan-zoom.min.js', 'r')
        PanZoomJS = PanZoom.read()
        PanZoom.close()
        f.write('''
        <body>
            <script type="text/javascript">''' + PanZoomJS + '''</script>
            <div class="Image">''' + SVGData + '''</div>
            <script type="text/javascript">
                var SVGImage = document.getElementById('SVGImage');
                SVGImage.setAttribute("height","100%");
                SVGImage.setAttribute("width","100%");
                SVGImage.removeAttribute("viewBox");

                svgPanZoom('#SVGImage', {
                  controlIconsEnabled: true,
                  zoomScaleSensitivity: 0.4,
                  minZoom: 0.5,
                  maxZoom: 10000,
                });
            </script>
        </body>
        ''')

        f.write('</html>')
