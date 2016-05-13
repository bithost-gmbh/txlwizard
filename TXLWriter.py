from .Patterns import Definitions
from .Patterns import Structure
import os.path

class TXLWriter(object):
    '''
    Controller class for generating TXL / SVG / HTML output.


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
        self.Definitions = Definitions.Definitions()

        #: int: Width of the sample in um. Used to draw coordinate system.
        self.Width = 800
        #: int: Height of the sample in um. Used to draw coordinate system.
        self.Height = 800

        #: int: Coordinate Sytem Grid Spacing in um.
        self.GridDistance = 100

        #: int: Coordinate Sytem Sub Grid Spacing in um.
        self.SubGridDistance = 10

        #: int: Width of the SVG Image in pixels
        self.SVGWidth = 800

        #: int: Height of the SVG Image in pixels
        self.SVGHeight = 800

        #: bool: Show the coordinate system or not
        self.ShowCoordinateSystem = True

        for i in ['Width','Height','GridDistance','SubGridDistance','ShowCoordinateSystem']:
            if i in kwargs:
                setattr(self,i,kwargs[i])

        self.ContentStructures = {}
        self.ContentStructuresIndexList = []
        self.HelperStructures = {}
        self.HelperStructuresIndexList = []
        if self.ShowCoordinateSystem:
            self.DrawCoordinateSystem()

    def DrawCoordinateSystem(self):
        '''
        Draws the coordinate system (grid and sub-grid)
        '''
        LineWidth = 10*1./2.


        CoordinateXAxis = self.AddHelperStructure('CoordinateXAxis')
        CoordinateXAxis.AddPattern('Polygon',Points=[
            [-self.Width/2,0],
            [self.Width/2,0]
        ],PathOnly = True,StrokeWidth = LineWidth)
        CoordinateYAxis = self.AddHelperStructure('CoordinateYAxis')
        CoordinateYAxis.AddPattern('Polygon',Points=[
            [0,-self.Height/2],
            [0,self.Height/2]
        ],PathOnly = True,StrokeWidth = LineWidth)

        Grids = {}

        for GridName in ['Grid','SubGrid']:
            Grid = self.AddHelperStructure(GridName)
            Grids[GridName] = Grid
            GridDistance = self.__getattribute__(GridName+'Distance')
            if GridName == 'SubGrid':
                LineWidth = 1./2.
            for i in range(0,int(round(self.Width/GridDistance/2))):
                for j in [-i*GridDistance,i*GridDistance]:
                    Grid.AddPattern('Polygon',Points=[
                        [1.*j,-self.Height/2.],
                        [1.*j,self.Height/2.]
                    ],PathOnly = True,StrokeWidth = LineWidth)
            for i in range(0,int(round(self.Height/GridDistance/2))):
                for j in [-i*GridDistance,i*GridDistance]:
                    Grid.AddPattern('Polygon',Points=[
                        [-self.Width/2.,1.*j],
                        [self.Width/2.,1.*j]
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
        self.HelperStructures[Index] = StructureObject
        self.HelperStructuresIndexList.append(Index)
        return self.HelperStructures[Index]

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
        self.ContentStructures[Index] = StructureObject
        self.ContentStructuresIndexList.append(Index)
        return self.ContentStructures[Index]


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
        self.Definitions.AddStructure(Index,StructureObject)
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
            self.GenerateTXLFile(Filename)

        if SVG:
            self.GenerateSVGFile(Filename)

        if HTML:
            self.GenerateHTMLFile(Filename)

    def GenerateTXLFile(self,Filename):
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
        f.write(self.Definitions.GetTXLOutput())
        f.write('\n\n'+'! ### Definitions End ###'+'\n\n')
        f.write('\n\n'+'! ### Content Structures Start ###'+'\n')
        for i in self.ContentStructuresIndexList:
            if self.ContentStructures[i].TXLOutput:
                f.write(self.ContentStructures[i].GetTXLOutput())
        f.write('\n\n'+'! ### Content Structures End ###'+'\n')

        f.write('ENDLIB')
        f.close()

    def GenerateSVGFile(self,Filename):
        #See https://developer.mozilla.org/en-US/docs/Web/SVG

        f = open(Filename+'.svg','w')
        f.write('<svg version="1.1" baseProfile="full" width="800" height="800" '+
                'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '+
                'id="SVGImage" viewBox="{:d} {:d} {:d} {:d}">'.format(int(-self.Width/2),int(-self.Height/2),int(self.Width),int(self.Height))+'\n')
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
        f.write(self.Definitions.GetSVGOutput())
        f.write('<g transform="translate({:1.2f},{:1.2f}),matrix(1,0,0,-1,0,0)">'.format(1.*self.SVGWidth/2.,1.*self.SVGHeight/2.)+'\n')
        f.write('<g id="HelperStructures">'+'\n')
        for i in self.HelperStructuresIndexList:
            f.write(self.HelperStructures[i].GetSVGOutput())
        f.write('</g>')
        f.write('<g id="ContentStructures">'+'\n')
        for i in self.ContentStructuresIndexList:
            f.write(self.ContentStructures[i].GetSVGOutput())
        f.write('</g>')
        f.write('</g>')
        f.write('</svg>')
        f.close()

    def GenerateHTMLFile(self,Filename):
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

