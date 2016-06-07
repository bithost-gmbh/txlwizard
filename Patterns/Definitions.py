'''
Implements a class for `Pattern` objects of type `Definitions`.
Intended for storing definition structures.
'''
import AbstractPattern


class Definitions(AbstractPattern.AbstractPattern):
    '''
    Implements a class for `Pattern` objects of type `Definitions`.\n
    Intended for storing definition structures.\n
    For internal use only.

    Parameters
    ----------
    **kwargs
        keyword arguments passed to the :class:`TXLWizard.Patterns.AbstractPattern.AbstractPattern` constructor.
    '''

    def __init__(self, **kwargs):
        super(Definitions, self).__init__(**kwargs)

        #: str: specifies the type of the pattern. Set to 'Definitions'
        self.Type = 'Definitions'

        #: dict: Dictionary of :class:`TXLWizard.Patterns.Structure.Structure` instances. The key is the ID of the structure.
        self.Structures = {}

        #: list of str: Index of the keys in `self.Structures`
        self.StructuresIndex = []

    def AddStructure(self, ID, Structure):
        '''
        Add a definition structure.

        Parameters
        ----------
        ID: str
            Unique identification of the structure
        Structure: :class:`TXLWizard.Patterns.Structure.Structure`
            `Structure` instance to be added
        '''
        self.Structures[ID] = Structure
        self.StructuresIndex.append(ID)

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
        SVG += '</defs>' + '\n'
        return SVG
