'''
Implements a class for `Pattern` objects of type `Circle` (`C`).\n
Renders a circle.
'''
import AbstractPattern
import math


class Circle(AbstractPattern.AbstractPattern):
    '''
    Implements a class for `Pattern` objects of type `Circle`.\n
    Corresponds to the TXL command `C` (`CP` if `PathOnly` is specified, `CPR` if `RoundCaps` and `CPE` if `Extended`).\n
    Renders a circle. \n
    Optionally, only a sector is shown when specifying `StartAngle` and `EndAngle`.\n
    If `NumberOfPoints` is given, the number of path segments defining the circle can be specified.\n
    If `PathOnly` is set to True, only the arc of the circle is shown. Optionally, the ends of the path are rounded by
    specifying `RoundCaps` or extended by specifying `Extended` along with `PathOnly`.

    Parameters
    ----------
    Center: list of float
        x- and y-coordinates specifying the center of the circle
    Radius: float
        Radius of the circle
    StartAngle: float, optional
        If given, only a sector is drawn from `StartAngle` to `EndAngle`.\n
        Defaults to None.
    EndAngle: float, optional
        If given, only a sector is drawn from `StartAngle` to `EndAngle`.\n
        Defaults to None.
    NumberOfPoints: int, optional
        Number of path segments used for drawing the circle.\n
        Defaults to None.
    PathOnly: bool, optional
        If set to True, only the arc of the circle is drawn.\n
        Defaults to False.
    RoundCaps: bool, optional
        If set to True along with `PathOnly`, the end of the path is rounded.\n
        Defaults to False.
    Extended: bool, optional
        If set to True along with `PathOnly`, the end of the path is extended.\n
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

    Create Content Structure for Circle and add Pattern of type `Circle`

    >>> CircleStructure = TXLWriter.AddContentStructure('MyCircleID')
    >>> CircleStructure.AddPattern(
    ...     'Circle',
    ...     Center=[0, 0],
    ...     Radius=50,
    ...     Layer=1
    ... ) #doctest: +ELLIPSIS
    <TXLWizard.Patterns.Circle.Circle object at 0x...>

    Generate Files

    >>> TXLWriter.GenerateFiles('Tests/Results/Patterns/Circle')

    '''

    def __init__(self, Center, Radius, **kwargs):
        super(Circle, self).__init__(**kwargs)

        #: str: specifies the type of the pattern. Set to 'Circle'
        self.Type = 'Circle'

        #: list of float: x- and y- coordinates of the origin point of the pattern
        self._OriginPoint = Center

        #: list of float: x- and y-coordinates specifying the center of the circle
        self.Center = Center

        #: float: Radius of the circle
        self.Radius = Radius

        #: float: If set, only a sector is drawn from `self.StartAngle` to `self.EndAngle`.
        self.StartAngle = None

        #: float: If set, only a sector is drawn from `self.StartAngle` to `self.EndAngle`.
        self.EndAngle = None

        #: int: Number of path segments used for drawing the circle.
        self.NumberOfPoints = None

        #: bool: If set to True, only the arc of the circle is drawn.
        self.PathOnly = False

        #: bool: If set to True along with `PathOnly`, the end of the path is rounded
        self.RoundCaps = False

        #: bool: If set to True along with `PathOnly`, the end of the path is extended
        self.Extended = False

        #: list of float: If `self.StartAngle` and `self.EndAngle` are set, the starting point of the segment arc is calculated
        self.StartPoint = None

        #: list of float: If `self.StartAngle` and `self.EndAngle` are set, the ending point of the segment arc is calculated
        self.EndPoint = None

        for i in ['StartAngle', 'EndAngle', 'NumberOfPoints', 'PathOnly', 'RoundCaps', 'Extended']:
            if i in kwargs:
                setattr(self, i, kwargs[i])

        if self.StartAngle != None and self.EndAngle != None:
            self.StartPoint = [math.cos(self.StartAngle / 360. * 2. * math.pi) * self.Radius,
                               math.sin(self.StartAngle / 360. * 2. * math.pi) * self.Radius]
            self.EndPoint = [math.cos(self.EndAngle / 360. * 2. * math.pi) * self.Radius,
                             math.sin(self.EndAngle / 360. * 2. * math.pi) * self.Radius]

    def GetTXLOutput(self):
        BoundaryString = ''
        BoundaryStringEnd = ''
        if self.PathOnly:
            BoundaryString = 'P'
            BoundaryStringEnd = BoundaryString
            if self.RoundCaps:
                BoundaryString += 'R'
            elif self.Extended:
                BoundaryString += 'E'
        TXL = ''
        TXL += 'C' + BoundaryString + ' '
        TXL += (
            '' + self._GetFloatFormatString() + ' ' + self._GetFloatFormatString() + ',' + self._GetFloatFormatString() + ' ').format(
            self.Radius, self.Center[0], self.Center[1])

        if self.StartAngle != None and self.EndAngle != None:
            if not self.PathOnly:
                TXL += '('
            TXL += ('' + self._GetFloatFormatString() + ' ' + self._GetFloatFormatString() + ' ').format(
                self.StartAngle, self.EndAngle)

            if self.NumberOfPoints != None:
                TXL += '{:d}'.format(self.NumberOfPoints)

            if not self.PathOnly:
                TXL += ') '

        TXL += 'ENDC' + BoundaryStringEnd + '\n'
        return TXL

    def GetSVGOutput(self):
        SVG = ''
        if self.StartAngle == None or abs(self.EndAngle - self.StartAngle) == 360:
            SVGAttributes = {
                # 'cx':'{:1.4f}'.format(self.Center[0]),
                # 'cy':'{:1.4f}'.format(self.Center[1]),
                'cx': '0',
                'cy': '0',
                'r': ('' + self._GetFloatFormatString() + '').format(
                    self.Radius),
            }
            if self.PathOnly:
                SVGAttributes['style'] = [
                    'fill:none',
                    ('stroke-width:' + self._GetFloatFormatString() + '').format(
                        self.Attributes['StrokeWidth'])
                ]
            SVG += ('<circle ' + self._GetSVGAttributesString(SVGAttributes) +
                    ' />' + '\n')
        else:
            LargeAngle = 0
            if abs(self.EndAngle - self.StartAngle) >= 180:
                LargeAngle = 1
            # See http://www.w3.org/TR/2003/REC-SVG11-20030114/paths.html#PathDataEllipticalArcCommands
            SweepFlag = 1
            SVGAttributes = {
                'd': ('m ' + self._GetFloatFormatString() + ' ' + self._GetFloatFormatString() + ' ').format(
                    self.StartPoint[0], self.StartPoint[1]) +
                     # 'l {:1.4f} {:1.4f} '.format(StartPoint[0], StartPoint[1])+
                     ('a ' + self._GetFloatFormatString() + ' ' + self._GetFloatFormatString() + ' 0 {:d} {:d} ' +
                      self._GetFloatFormatString() + ' ' + self._GetFloatFormatString() + ' ').format(
                         self.Radius, self.Radius, LargeAngle, SweepFlag,
                         self.EndPoint[0] - self.StartPoint[0],
                         self.EndPoint[1] - self.StartPoint[1])
                # 'l {:1.4f} {:1.4f}'.format(self.Center[0],self.Center[1])
            }
            if self.PathOnly:
                SVGAttributes['style'] = [
                    'fill:none',
                    ('stroke-width:' + self._GetFloatFormatString() + '').format(
                        self.Attributes['StrokeWidth'])
                ]
                if self.RoundCaps:
                    SVGAttributes['stroke-linecap'] = 'round'
                elif self.Extended:
                    SVGAttributes['stroke-linecap'] = 'square'

            SVG += ('<path ' + self._GetSVGAttributesString(SVGAttributes) + ' />')
        return SVG
