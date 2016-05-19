'''
Implements a class for `Pattern` objects of type `Reference` (`SREF`).\n
Renders a copy of the referenced structure.
'''
import AbstractPattern


class Reference(AbstractPattern.AbstractPattern):
    '''
    Implements a class for `Pattern` objects of type `Reference`.\n
    Corresponds to the TXL command `SREF`.\n
    Renders a copy of the structure identified by `ReferencedStructureID` at `OriginPoint`.

    Parameters
    ----------
    ReferencedStructureID: str
            ID of the structure being referenced to
    OriginPoint: list of float
        x- and y-coordinates of the starting point
    **kwargs
        keyword arguments passed to the :class:`TXLWizard.Patterns.AbstractPattern.AbstractPattern` constructor.
        Can specify attributes of the current pattern.
    '''

    def __init__(self, ReferencedStructureID, OriginPoint, **kwargs):
        super(Reference, self).__init__(**kwargs)

        #: str: specifies the type of the pattern. Set to 'Reference'
        self.Type = 'Reference'

        #: str: ID of the structure being referenced to
        self.ReferencedStructureID = ReferencedStructureID

        #: list of float: x- and y- coordinates of the origin point of the pattern
        self._OriginPoint = OriginPoint


    def GetTXLOutput(self):
        TXL = ''
        TXL += 'SREF ' + self.ReferencedStructureID + ' '
        TXL += '{:1.4f},{:1.4f} '.format(
            self._OriginPoint[0], self._OriginPoint[1]
        )
        TXL += '' + '\n'
        return TXL

    def GetSVGOutput(self):
        SVG = ''
        SVG += '<use ' + self._GetSVGAttributesString({
            'xlink:href': '#' + self.ReferencedStructureID.replace('+', ''),
            # 'x':'{:1.4f}'.format(self._OriginPoint[0]),
            # 'y':'{:1.4f}'.format(self._OriginPoint[1])
        }) + '/>' + '\n'
        return SVG
