'''
Implements a class for `Pattern` objects of type `Polygon` (`B`).\n
Renders an polygon.
'''
import AbstractPattern


class Polygon(AbstractPattern.AbstractPattern):
    '''
    Implements a class for `Pattern` objects of type `Polygon`.\n
    Corresponds to the TXL command `B`\n
    Renders an polygon. \n
    The boundary is always closed so the last point connects to the starting point

    Parameters
    ----------
    Points: list of list of float
        List of points (each point is a list of float, specifying the x- and y-coordinate of the point) that define the polygon
    **kwargs
        keyword arguments passed to the :class:`TXLWizard.Patterns.AbstractPattern.AbstractPattern` constructor.
        Can specify attributes of the current pattern.

    Examples
    --------

    Initialize TXLWriter

    >>> TXLWriter = TXLWizard.TXLWriter.TXLWriter()

    Create Content Structure for polygon and add Pattern of type `Polygon`

    >>> PolygonStructure = TXLWriter.AddContentStructure('MyPolygonID')
    >>> PolygonStructure.AddPattern(
    >>>     'Polygon',
    >>>     Points=[[0,0], [0,10], [20,50], [0,0]],
    >>>     Layer=1
    >>> )

    Complex structures can easily be added by generating the polygon points

    >>> import math
    >>> PolygonPoints = []
    >>> Radius = 5.
    >>> for i in range(21):
    >>>     # AngleRadians goes from 0 to pi in 20 steps
    >>>     AngleRadians = 0.5*2.*math.pi*1./20.*i
    >>>     PolygonPoints.append([
    >>>         Radius*math.cos(AngleRadians),Radius*math.sin(AngleRadians)
    >>>     ])
    >>> PolygonPoints.append([-20,-30])
    >>> PolygonPoints.append([20,-30])
    >>>
    >>> PolygonStructure.AddPattern(
    >>>     'Polygon',
    >>>     Points=PolygonPoints,
    >>>     Layer=1
    >>> )
    '''

    def __init__(self, Points, **kwargs):
        super(Polygon, self).__init__(**kwargs)

        #: str: specifies the type of the pattern. Set to 'Polygon'
        self.Type = 'Polygon'

        #: list of float: x- and y- coordinates of the origin point of the pattern
        self._OriginPoint = [0, 0]

        #: list of list of float: List of points (each point is a list of float, specifying the x- and y-coordinate of the point) that define the polygon
        self.Points = Points

    def GetTXLOutput(self):
        CommandString = 'B'
        EndCommandString = CommandString
        TXL = ''
        TXL += CommandString + ' '
        for Point in self.Points:
            TXL += (''+self._GetFloatFormatString()+','+self._GetFloatFormatString()+' ').format(Point[0], Point[1])
        TXL += 'END' + EndCommandString + '\n'
        return TXL

    def GetSVGOutput(self):
        SVG = ''

        PointsString = ''
        for Point in self.Points:
            PointsString += (''+self._GetFloatFormatString()+','+self._GetFloatFormatString()+' ').format(Point[0], Point[1])
        SVGAttributes = {'points': PointsString}
        SVG += '<polygon ' + self._GetSVGAttributesString(SVGAttributes) + ' />' + '\n'

        return SVG
