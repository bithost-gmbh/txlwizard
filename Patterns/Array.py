'''
Implements a class for `Pattern` objects of type `Array` (`AREF`).\n
Replicates the referenced structure in two directions.
'''
import AbstractPattern


class Array(AbstractPattern.AbstractPattern):
    '''
    Implements a class for `Pattern` objects of type `Array`.\n
    Corresponds to the TXL command `AREF`.\n
    Replicates the referenced structure `ReferencedStructureID` in two directions `PositionDelta1` and `PositionDelta2`
    for the number of times specified in `Repetitions1` and `Repetitions2`,
    starting at `OriginPoint`.\n
    The x- and y-coordinates of the replicated objects are calculated as follows:
    `OriginPoint+i*PositionDelta1+j*PositionDelta2`
    where `i` is an integer that ranges from 0 to `Repetitions1`
    and `j` is an integer that ranges from 0 to `Repetitions2`

    Parameters
    ----------
    ReferencedStructureID: str
        ID of the structure being referenced to
    OriginPoint: list of float
        x- and y- coordinates of the starting point
    PositionDelta1: list of float
        x- and y- coordinates of the first replication direction.
    PositionDelta2: list of float
        x- and y- coordinates of the second replication direction.
    Repetitions1: int
        Number of replications in the first replication direction
    Repetitions2: int
        Number of replications in the second replication direction
    **kwargs
        keyword arguments passed to the :class:`TXLWizard.Patterns.AbstractPattern.AbstractPattern` constructor.
        Can specify attributes of the current pattern.


    '''

    def __init__(self, ReferencedStructureID, OriginPoint, PositionDelta1, PositionDelta2, Repetitions1, Repetitions2,
                 **kwargs):

        super(Array, self).__init__(**kwargs)

        #: str: specifies the type of the pattern. Set to 'Array'
        self.Type = 'Array'

        #: str: ID of the structure being referenced to
        self.ReferencedStructureID = ReferencedStructureID

        #: list of float: x- and y- coordinates of the origin point of the pattern
        self._OriginPoint = OriginPoint

        #: list of float: x- and y- coordinates of the first replication direction.
        self.PositionDelta1 = PositionDelta1

        #: list of float: x- and y- coordinates of the second replication direction.
        self.PositionDelta2 = PositionDelta2

        #: int: Number of replications in the first replication direction
        self.Repetitions1 = Repetitions1

        #: int: Number of replications in the second replication direction
        self.Repetitions2 = Repetitions2

    def GetTXLOutput(self):
        TXL = ''
        if self.Repetitions1 > 1 or self.Repetitions2 > 1:
            TXL += 'AREF ' + self.ReferencedStructureID + ' '
            TXL += '({:1.4f},{:1.4f}) {:d} ({:1.4f},{:1.4f}) {:d} ({:1.4f},{:1.4f})'.format(
                self._OriginPoint[0], self._OriginPoint[1],
                self.Repetitions1, self.PositionDelta1[0], self.PositionDelta1[1],
                self.Repetitions2, self.PositionDelta2[0], self.PositionDelta2[1]
            )
            TXL += '' + '\n'
        else:
            TXL += 'SREF ' + self.ReferencedStructureID + ' '
            TXL += '{:1.4f} {:1.4f}'.format(
                self._OriginPoint[0], self._OriginPoint[1]
            )
            TXL += '' + '\n'
        return TXL

    def GetSVGOutput(self):
        SVG = ''
        for i in range(self.Repetitions1):
            for j in range(self.Repetitions2):
                OriginPoint = [
                    i * self.PositionDelta1[0] + j * self.PositionDelta2[0],
                    i * self.PositionDelta1[1] + j * self.PositionDelta2[1]
                ]
                SVGAttributes = self._GetSVGAttributesString({
                    'transform': ['translate({:1.4f},{:1.4f})'.format(OriginPoint[0], OriginPoint[1])]
                })
                SVG += (
                           '<g ' + SVGAttributes + '>' +
                           '<use ' + self.ParentStructure._GetPatternSVGAttributesString('Reference', self.Attributes, {
                               'xlink:href': '#' + self.ReferencedStructureID.replace('+', ''),
                               # 'x':'{:1.4f}'.format(i*self.PositionDelta1[0]+j*self.PositionDelta2[0]),
                               # 'y':'{:1.4f}'.format(i*self.PositionDelta1[1]+j*self.PositionDelta2[1])
                           }) + '/>' +
                           '</g>') + '\n'
        return SVG
