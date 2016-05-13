from . import AbstractPattern
class Definitions(AbstractPattern.AbstractPattern):
    def __init__(self,**kwargs):
        super(Definitions, self).__init__(**kwargs)
        self.Type = 'Definitions'
        self.Structures = {}
        self.StructuresIndex = []

    def AddStructure(self,Index,Structure):
        self.Structures[Index] = Structure
        self.StructuresIndex.append(Index)

    def GetTXLOutput(self):
        TXL = ''
        for i in self.StructuresIndex:
            if self.Structures[i].TXLOutput:
                TXL += self.Structures[i].GetTXLOutput()
        return TXL


    def GetSVGOutput(self):
        SVG = ''
        SVG += '<defs>'
        for i in self.StructuresIndex:
            SVG += self.Structures[i].GetSVGOutput()
        SVG += '</defs>'+'\n'
        return SVG