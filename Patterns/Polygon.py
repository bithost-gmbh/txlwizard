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
            TXL += '{:1.4f},{:1.4f} '.format(Point[0], Point[1])
        TXL += 'END' + EndCommandString + '\n'
        return TXL

    def GetSVGOutput(self):
        SVG = ''

        PointsString = ''
        for Point in self.Points:
            PointsString += '{:1.4f},{:1.4f} '.format(Point[0], Point[1])
        SVGAttributes = {'points': PointsString}
        SVG += '<polygon ' + self._GetSVGAttributesString(SVGAttributes) + ' />' + '\n'

        return SVG
