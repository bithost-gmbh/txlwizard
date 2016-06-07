'''
Implements a class for `Pattern` objects of type `Ellipse` (`ELP`).\n
Renders an ellipse.
'''
import AbstractPattern
import math


class Ellipse(AbstractPattern.AbstractPattern):
    '''
    Implements a class for `Pattern` objects of type `Ellipse`.\n
    Corresponds to the TXL command `ELP`.\n
    Renders an ellipse. Optionally, only a sector is shown when specifying `StartAngle` and `EndAngle`.\n
    If `NumberOfPoints` is given, the number of path segments defining the ellipse can be specified.\n
    If `PathOnly` is set to True, only the arc of the ellipse is shown.

    Parameters
    ----------
    Center: list of float
        x- and y-coordinates specifying the center of the ellipse
    RadiusX: float
        Semi-major axis of the ellipse in x-direction
    RadiusY: float
        Semi-minor axis of the ellipse in y-direction
    StartAngle: float, optional
        If given, only a sector is drawn from `StartAngle` to `EndAngle`.\n
        Defaults to 0
    EndAngle: float, optional
        If given, only a sector is drawn from `StartAngle` to `EndAngle`.\n
        Defaults to 0
    NumberOfPoints: int, optional
        Number of path segments used for drawing the ellipse.\n
        Defaults to None.
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

    Create Content Structure for ellipse and add Pattern of type `Ellipse`

    >>> EllipseStructure = TXLWriter.AddContentStructure('MyEllipseID')
    >>> EllipseStructure.AddPattern(
    ...     'Ellipse',
    ...     Center=[0, 0],
    ...     RadiusX=50,
    ...     RadiusY=70,
    ...     Layer=1
    ... ) #doctest: +ELLIPSIS
    <TXLWizard.Patterns.Ellipse.Ellipse object at 0x...>

    Generate Files

    >>> TXLWriter.GenerateFiles('Tests/Results/Patterns/Ellipse')

    '''

    def __init__(self, Center, RadiusX, RadiusY, **kwargs):
        super(Ellipse, self).__init__(**kwargs)

        #: str: specifies the type of the pattern. Set to 'Ellipse'
        self.Type = 'Ellipse'

        #: list of float: x- and y- coordinates of the origin point of the pattern
        self._OriginPoint = Center

        #: list of float: x- and y-coordinates specifying the center of the ellipse
        self.Center = Center

        #: float: Semi-major axis of the ellipse in x-direction
        self.RadiusX = RadiusX

        #: float: Semi-minor axis of the ellipse in y-direction
        self.RadiusY = RadiusY

        #: float: If given, only a sector is drawn from `StartAngle` to `EndAngle`.
        self.StartAngle = 0

        #: float: If given, only a sector is drawn from `StartAngle` to `EndAngle`.
        self.EndAngle = 360

        #: int: Number of path segments used for drawing the ellipse.
        self.NumberOfPoints = None

        #: list of float: If `self.StartAngle` and `self.EndAngle` are set, the starting point of the segment arc is calculated
        self.StartPoint = None

        #: list of float: If `self.StartAngle` and `self.EndAngle` are set, the ending point of the segment arc is calculated
        self.EndPoint = None

        for i in ['StartAngle', 'EndAngle', 'NumberOfPoints']:
            if i in kwargs:
                setattr(self, i, kwargs[i])

        if self.StartAngle != None and self.EndAngle != None:
            self.StartPoint = [math.cos(self.StartAngle / 360. * 2. * math.pi) * self.RadiusX,
                               math.sin(self.StartAngle / 360. * 2. * math.pi) * self.RadiusY]
            self.EndPoint = [math.cos(self.EndAngle / 360. * 2. * math.pi) * self.RadiusX,
                             math.sin(self.EndAngle / 360. * 2. * math.pi) * self.RadiusY]

    def GetTXLOutput(self):

        TXL = ''
        TXL += 'ELP '
        TXL += ('' + self._GetFloatFormatString() + ' ' + self._GetFloatFormatString() + ' ' +
                self._GetFloatFormatString() + ',' + self._GetFloatFormatString() + ' ').format(
            self.RadiusX, self.RadiusY,
            self.StartPoint[0], self.StartPoint[1])

        if self.StartAngle != None and self.EndAngle != None:
            TXL += ('' + self._GetFloatFormatString() + ' ' + self._GetFloatFormatString() + ' ').format(
                self.StartAngle, self.EndAngle)

            if self.NumberOfPoints != None:
                TXL += '{:d}'.format(self.NumberOfPoints)

        TXL += 'ENDELP' + '\n'
        return TXL

    def GetSVGOutput(self):

        SVG = ''
        if self.StartAngle == None or abs(self.EndAngle - self.StartAngle) == 360:
            SVG += ('<ellipse ' + self._GetSVGAttributesString({
                # 'cx':'{:1.4f}'.format(self.Center[0]),
                # 'cy':'{:1.4f}'.format(self.Center[1]),
                'cx': '0',
                'cy': '0',
                'rx': ('' + self._GetFloatFormatString() + '').format(self.RadiusX),
                'ry': ('' + self._GetFloatFormatString() + '').format(self.RadiusY),
            }) +
                    ' />' + '\n')
        else:
            # See http://www.w3.org/TR/2003/REC-SVG11-20030114/paths.html#PathDataEllipticalArcCommands
            LargeAngle = 0
            if abs(self.EndAngle - self.StartAngle) >= 180:
                LargeAngle = 1
            SVG += ('<path ' + self._GetSVGAttributesString({
                'd': ('m ' + self._GetFloatFormatString() + ' ' + self._GetFloatFormatString() + ' ').format(
                    self.StartPoint[0], self.StartPoint[1]) +
                     # 'l {:1.4f} {:1.4f} '.format(self.StartPoint[0], self.StartPoint[1])+
                     ('a ' + self._GetFloatFormatString() + ' ' + self._GetFloatFormatString() + ' 0 0 ' +
                      '{:d} ' + self._GetFloatFormatString() + ' ' + self._GetFloatFormatString() + ' ').format(
                         self.RadiusX, self.RadiusY,
                         LargeAngle, self.EndPoint[0] - self.StartPoint[0], self.EndPoint[1] - self.StartPoint[1])
                # 'l {:1.4f} {:1.4f}'.format(self.Center[0],self.Center[1])
            }) + ' />')
        return SVG
