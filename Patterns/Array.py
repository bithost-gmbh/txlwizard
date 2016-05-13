from . import AbstractPattern
class Array(AbstractPattern.AbstractPattern):
    def __init__(self, ReferencedStructureID, OriginPoint, PositionDelta1, PositionDelta2, Repetitions1, Repetitions2, **kwargs):
        super(Array, self).__init__(**kwargs)
        self.Type = 'Array'
        self.ReferencedStructureID = ReferencedStructureID
        self.OriginPoint = OriginPoint
        self.PositionDelta1 = PositionDelta1
        self.PositionDelta2 = PositionDelta2
        self.Repetitions1 = Repetitions1
        self.Repetitions2 = Repetitions2

    def GetTXLOutput(self):
        TXL = ''
        if self.Repetitions1 > 1 or self.Repetitions2 > 1:
            TXL += 'AREF '+self.ReferencedStructureID+' '
            TXL += '({:1.4f},{:1.4f}) {:d} ({:1.4f},{:1.4f}) {:d} ({:1.4f},{:1.4f})'.format(
                self.OriginPoint[0],self.OriginPoint[1],
                self.Repetitions1, self.PositionDelta1[0], self.PositionDelta1[1],
                self.Repetitions2, self.PositionDelta2[0], self.PositionDelta2[1]
            )
            TXL += ''+'\n'
        else:
            TXL += 'SREF '+self.ReferencedStructureID+' '
            TXL += '{:1.4f} {:1.4f}'.format(
                self.OriginPoint[0],self.OriginPoint[1]
            )
            TXL += ''+'\n'
        return TXL


    def GetSVGOutput(self):
        SVG = ''
        for i in range(self.Repetitions1):
            for j in range(self.Repetitions2):
                OriginPoint = [
                    i*self.PositionDelta1[0]+j*self.PositionDelta2[0],
                    i*self.PositionDelta1[1]+j*self.PositionDelta2[1]
                ]
                SVGAttributes = self.GetSVGAttributesString({
                            'transform':['translate({:1.4f},{:1.4f})'.format(OriginPoint[0],OriginPoint[1])]
                        })
                SVG += (
                   '<g '+SVGAttributes+'>'+
                        '<use '+self.ParentStructure.GetPatternSVGAttributesString('Reference',self.Attributes,{
                            'xlink:href':'#'+self.ReferencedStructureID.replace('+',''),
                            #'x':'{:1.4f}'.format(i*self.PositionDelta1[0]+j*self.PositionDelta2[0]),
                            #'y':'{:1.4f}'.format(i*self.PositionDelta1[1]+j*self.PositionDelta2[1])
                        })+'/>'+
                    '</g>')+'\n'
        return SVG