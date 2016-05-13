from .Patterns import Definitions
from .Patterns import Structure
import os.path

class TXLWriter(object):
    '''
    Controller class for generating TXL / SVG / HTML output.
    Here we can add structures (definitions and content) which will be rendered in the output.
    '''
    def __init__(self,**kwargs):
        '''
        Constructor

        Parameters
        ----------
        Width : Optional[int],
            Width of the sample in um. Used to draw coordinate system.
        Height : Optional[int]
            Height of the sample in um. Used to draw coordinate system.
        ShowCoordinateSystem : Optional[bool]
            Show the coordinate system or not
        GridDistance : Optional[int]
            Coordinate Sytem Grid Spacing in um.
        SubGridDistance : Optional[int]
            Coordinate System Sub-Grid Spacing in um

        '''

        #: :class:`Definitions`: container for definition structures
        self._Definitions = Definitions.Definitions()

        #: int: Width of the sample in um. Used to draw coordinate system.
        self._Width = 800
        #: int: Height of the sample in um. Used to draw coordinate system.
        self._Height = 800

        #: int: Coordinate Sytem Grid Spacing in um.
        self._GridDistance = 100

        #: int: Coordinate Sytem Sub Grid Spacing in um.
        self._SubGridDistance = 10

        #: int: Width of the SVG Image in pixels
        self._SVGWidth = 800

        #: int: Height of the SVG Image in pixels
        self._SVGHeight = 800

        #: bool: Show the coordinate system or not
        self._ShowCoordinateSystem = True

        #: dict: dictionary of all content structures
        self._ContentStructures = {}

        #: List[str]: list of indices of content structures, needed for correct order
        self._ContentStructuresIndexList = []

        #: dict: dictionary of all helper structures
        self._HelperStructures = {}

        #: List[str]: list of indices of helper structures, needed for correct order
        self._HelperStructuresIndexList = []

        for i in ['Width','Height','GridDistance','SubGridDistance','ShowCoordinateSystem']:
            if i in kwargs:
                setattr(self,i,kwargs[i])

        if self._ShowCoordinateSystem:
            self._DrawCoordinateSystem()

    def _DrawCoordinateSystem(self):
        '''
        Draws the coordinate system (grid and sub-grid)
        '''
        LineWidth = 10*1./2.


        CoordinateXAxis = self.AddHelperStructure('CoordinateXAxis')
        CoordinateXAxis.AddPattern('Polygon',Points=[
            [-self._Width/2,0],
            [self._Width/2,0]
        ],PathOnly = True, StrokeWidth = LineWidth)

        CoordinateYAxis = self.AddHelperStructure('CoordinateYAxis')
        CoordinateYAxis.AddPattern('Polygon',Points=[
            [0,-self._Height/2],
            [0,self._Height/2]
        ],PathOnly = True, StrokeWidth = LineWidth)

        Grids = {}

        for GridName in ['Grid','SubGrid']:
            Grid = self.AddHelperStructure(GridName)
            Grids[GridName] = Grid
            GridDistance = self.__getattribute__('_'+GridName+'Distance')
            if GridName == 'SubGrid':
                LineWidth = 1./2.
            for i in range(0,int(round(self._Width/GridDistance/2))):
                for j in [-i*GridDistance,i*GridDistance]:
                    Grid.AddPattern('Polygon',Points=[
                        [1.*j,-self._Height/2.],
                        [1.*j,self._Height/2.]
                    ],PathOnly = True,StrokeWidth = LineWidth)
            for i in range(0,int(round(self._Height/GridDistance/2))):
                for j in [-i*GridDistance,i*GridDistance]:
                    Grid.AddPattern('Polygon',Points=[
                        [-self._Width/2.,1.*j],
                        [self._Width/2.,1.*j]
                    ],PathOnly = True,StrokeWidth = LineWidth)


    def AddHelperStructure(self, Index, **kwargs):
        '''
        Add helper structure. Helper structures are only visible in the HTML / SVG Output.

        Parameters
        ----------
        Index: str
            Identification of the structure
        kwargs: dict
            keyword arguments passed to the structure constructor

        Returns
        -------
        :class:`Structure` structure instance

        '''
        StructureObject = Structure.Structure(Index,**kwargs)
        self._HelperStructures[Index] = StructureObject
        self._HelperStructuresIndexList.append(Index)
        return self._HelperStructures[Index]

    def AddContentStructure(self, Index, **kwargs):
        '''
        Add content structure. A content structure can hold patterns that will render in the output.

        Parameters
        ----------
        Index: str
            Identification of the structure
        kwargs: dict
            keyword arguments passed to the structure constructor

        Returns
        -------
        :class:`Structure` structure instance

        '''
        StructureObject = Structure.Structure(Index,**kwargs)
        self._ContentStructures[Index] = StructureObject
        self._ContentStructuresIndexList.append(Index)
        return self._ContentStructures[Index]


    def AddDefinitionStructure(self, Index, **kwargs):
        '''
        Add definition structure. A definition structure can be referenced by a content structure

        Parameters
        ----------
        Index: str
            Identification of the structure
        kwargs: dict
            keyword arguments passed to the structure constructor

        Returns
        -------
        :class:`Structure` structure instance

        '''
        StructureObject = Structure.Structure(Index,**kwargs)
        self._Definitions.AddStructure(Index,StructureObject)
        return StructureObject

    def GenerateFiles(self,Filename,TXL=True,SVG=True,HTML=True):
        '''
        Generate the output files.

        Parameters
        ----------
        Filename: str
            Path / Filename without extension.
            The corresponding path will be created if it does not exist
        TXL: Optional[bool]
            Enable TXL Output
        SVG: Optional[bool]
            Enable SVG Output
        HTML: Optional[bool]
            Enable HTML Output


        '''
        Path = os.path.dirname(Filename)
        if len(Path) and not os.path.exists(Path):
            os.makedirs(Path)

        if TXL:
            self._GenerateTXLFile(Filename)

        if SVG:
            self._GenerateSVGFile(Filename)

        if HTML:
            self._GenerateHTMLFile(Filename)

    def _GenerateTXLFile(self,Filename):
        '''
        Generate the TXL file.

        Parameters
        ----------
        Filename: str
            Path / Filename without extension.

        '''
        f = open(Filename+'.txl','w')
        f.write('LETXTLIB 1.0.0'+'\n')
        f.write('UNIT MICRON'+'\n')
        f.write('RESOLVE 0.0001'+'\n')
        f.write('BEGLIB'+'\n')
        f.write('\n\n'+'! ### Definitions Start ###'+'\n')
        f.write(self._Definitions.GetTXLOutput())
        f.write('\n\n'+'! ### Definitions End ###'+'\n\n')
        f.write('\n\n'+'! ### Content Structures Start ###'+'\n')
        for i in self._ContentStructuresIndexList:
            if self._ContentStructures[i].TXLOutput:
                f.write(self._ContentStructures[i].GetTXLOutput())
        f.write('\n\n'+'! ### Content Structures End ###'+'\n')

        f.write('ENDLIB')
        f.close()

    def _GenerateSVGFile(self,Filename):
        '''
        Generate the TXL file.

        Parameters
        ----------
        Filename: str
            Path / Filename without extension.

        '''
        #See https://developer.mozilla.org/en-US/docs/Web/SVG

        f = open(Filename+'.svg','w')
        f.write('<svg version="1.1" baseProfile="full" width="800" height="800" '+
                'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '+
                'id="SVGImage" viewBox="{:d} {:d} {:d} {:d}">'.format(int(-self._Width/2),int(-self._Height/2),int(self._Width),int(self._Height))+'\n')
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
        f.write('<g transform="translate({:1.2f},{:1.2f}),matrix(1,0,0,-1,0,0)">'.format(1.*self._SVGWidth/2.,1.*self._SVGHeight/2.)+'\n')
        f.write('<g id="HelperStructures">'+'\n')
        for i in self._HelperStructuresIndexList:
            f.write(self._HelperStructures[i].GetSVGOutput())
        f.write('</g>')
        f.write('<g id="ContentStructures">'+'\n')
        for i in self._ContentStructuresIndexList:
            f.write(self._ContentStructures[i].GetSVGOutput())
        f.write('</g>')
        f.write('</g>')
        f.write('</svg>')
        f.close()

    def _GenerateHTMLFile(self,Filename):
        '''
        Generate the TXL file.

        Parameters
        ----------
        Filename: str
            Path / Filename without extension.

        '''
        f = open(Filename+'.svg','r')
        SVGData = f.read()
        f.close()

        f = open(Filename+'.html','w')
        f.write('<html>')
        f.write('''
        <head>
            <style>
                body{margin:0px;padding:0px;}
                #SVGImage {box-sizing:border-box;-moz-box-sizing:border-box;-ms-box-sizing:border-box;}
            </style>
        </head>
        ''')
        PanZoom = open(os.path.dirname(__file__)+'/Helpers/svg-pan-zoom.min.js','r')
        PanZoomJS = PanZoom.read()
        PanZoom.close()
        f.write('''
        <body>
            <script type="text/javascript">'''+PanZoomJS+'''</script>
            <div class="Image">'''+SVGData+'''</div>
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

