from . import AbstractPattern
class Reference(AbstractPattern.AbstractPattern):
    def __init__(self, ReferencedStructureID, OriginPoint, **kwargs):
        super(Reference, self).__init__(**kwargs)
        self.Type = 'Reference'
        self.ReferencedStructureID = ReferencedStructureID
        self.OriginPoint = OriginPoint


    def GetTXLOutput(self):
        TXL = ''
        TXL += 'SREF '+self.ReferencedStructureID+' '
        TXL += '{:1.4f},{:1.4f} '.format(
            self.OriginPoint[0],self.OriginPoint[1]
        )
        TXL += ''+'\n'
        return TXL


    def GetSVGOutput(self):
        SVG = ''
        SVG += '<use '+self.GetSVGAttributesString({
            'xlink:href':'#'+self.ReferencedStructureID.replace('+',''),
            #'x':'{:1.4f}'.format(self.OriginPoint[0]),
            #'y':'{:1.4f}'.format(self.OriginPoint[1])
        })+'/>'+'\n'
        return SVG