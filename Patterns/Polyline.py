'''
Module `TXLWizard.Patterns.Polyline` contains the :class:`TXLWizard.Patterns.Polyline.Polyline` class
'''

from . import AbstractPattern


class Polyline(AbstractPattern.AbstractPattern):
    '''
    Implements a class for `Pattern` objects of type `Polyline`.
    Corresponds to the TXL command `P` (``PR` if `RoundCaps` is True).
    Renders an path specified by points
    The ends can be rounded by specifying `RoundCaps`

    Parameters
    ----------
    Points: list of list of float
        List of points (each point is a list of float, specifying the x- and y-coordinate of the point) that define the path
    RoundCaps: bool, optional
        If set to True, the end of the path is rounded.
        Defaults to False.
    **kwargs
        keyword arguments passed to the :class:`TXLWizard.Patterns.AbstractPattern.AbstractPattern` constructor.
        Can specify attributes of the current pattern.
    '''

    def __init__(self, Points, **kwargs):
        super(Polyline, self).__init__(**kwargs)

        #: str: specifies the type of the pattern. Set to 'Polyline'
        self.Type = 'Polyline'

        #: list of float: x- and y- coordinates of the origin point of the pattern
        self._OriginPoint = [0, 0]

        #: list of list of float: List of points (each point is a list of float, specifying the x- and y-coordinate of the point) that define the polygon
        self.Points = Points

        #: bool: If set to True, the end of the path is rounded
        self.RoundCaps = False

        for i in ['RoundCaps']:
            if i in kwargs:
                setattr(self, i, kwargs[i])

    def GetTXLOutput(self):
        CommandString = 'P'
        EndCommandString = CommandString
        if self.RoundCaps:
            CommandString += 'R'
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
        SVGAttributes['style'] = ['fill:none']
        if self.Attributes['StrokeWidth'] != None:
            SVGAttributes['style'].append('stroke-width:{:1.4f}'.format(self.Attributes['StrokeWidth']))
        if self.RoundCaps:
            SVGAttributes['stroke-linecap'] = 'round'
        SVG += '<polyline ' + self._GetSVGAttributesString(SVGAttributes) + ' />' + '\n'

        return SVG
