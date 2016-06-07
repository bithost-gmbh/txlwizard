'''
Implements a class for `Pattern` objects of type `Polyline` (`B`).\n
Renders an path specified by points.
'''

import AbstractPattern


class Polyline(AbstractPattern.AbstractPattern):
    '''
    Implements a class for `Pattern` objects of type `Polyline`.\n
    Corresponds to the TXL command `P` (`PR` if `RoundCaps` is True).\n
    Renders an path specified by points.\n
    The ends can be rounded by specifying `RoundCaps`

    Parameters
    ----------
    Points: list of list of float
        List of points (each point is a list of float, specifying the x- and y-coordinate of the point) that define the path
    RoundCaps: bool, optional
        If set to True, the end of the path is rounded.\n
        Defaults to False.
    **kwargs
        keyword arguments passed to the :class:`TXLWizard.Patterns.AbstractPattern.AbstractPattern` constructor.
        Can specify attributes of the current pattern.
        
        
    Examples
    --------

    IGNORE:

        >>> import sys
        >>> import os.path
        >>> sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../../'))

    IGNORE

    Import required modules

    >>> import TXLWizard.TXLWriter

    Initialize TXLWriter

    >>> TXLWriter = TXLWizard.TXLWriter.TXLWriter()

    Create Content Structure for polyline and add Pattern of type `Polyline`

    >>> PolylineStructure = TXLWriter.AddContentStructure('MyPolylineID')
    >>> PolylineStructure.AddPattern(
    ...     'Polyline',
    ...     Points=[[0,0], [0,10], [20,50], [0,0]],
    ...     StrokeWidth=3,
    ...     Layer=1
    ... ) #doctest: +ELLIPSIS
    <TXLWizard.Patterns.Polyline.Polyline object at 0x...>

    Complex structures can easily be added by generating the Polyline points

    >>> import math
    >>> PolylinePoints = []
    >>> Radius = 10.
    >>> for i in range(21):
    ...     # AngleRadians goes from 0 to pi in 20 steps
    ...     AngleRadians = 0.5*2.*math.pi*1./20.*i
    ...     PolylinePoints.append([
    ...         Radius*math.cos(AngleRadians),Radius*math.sin(AngleRadians)
    ...     ])
    >>> PolylinePoints.append([-20,-30])
    >>> PolylinePoints.append([20,-30])
    >>>
    >>> PolylineStructure.AddPattern(
    ...     'Polyline',
    ...     Points=PolylinePoints,
    ...     RoundCaps=True,
    ...     StrokeWidth=3,
    ...     Layer=1
    ... ) #doctest: +ELLIPSIS
    <TXLWizard.Patterns.Polyline.Polyline object at 0x...>

    Generate Files

    >>> TXLWriter.GenerateFiles('Tests/Results/Patterns/Polyline')
    
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
            TXL += ('' + self._GetFloatFormatString() + ',' + self._GetFloatFormatString() + ' ').format(Point[0],
                                                                                                         Point[1])
        TXL += 'END' + EndCommandString + '\n'
        return TXL

    def GetSVGOutput(self):
        SVG = ''

        PointsString = ''
        for Point in self.Points:
            PointsString += ('' + self._GetFloatFormatString() + ',' + self._GetFloatFormatString() + ' ').format(
                Point[0], Point[1])
        SVGAttributes = {'points': PointsString}
        SVGAttributes['style'] = ['fill:none']

        if self.Attributes['StrokeWidth'] != None:
            SVGAttributes['style'].append(
                ('stroke-width:' + self._GetFloatFormatString() + '').format(self.Attributes['StrokeWidth']))
        if self.RoundCaps:
            SVGAttributes['stroke-linecap'] = 'round'
        SVG += '<polyline ' + self._GetSVGAttributesString(SVGAttributes) + ' />' + '\n'

        return SVG
