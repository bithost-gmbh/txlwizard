'''
Provides an abstract class for `Pattern` objects
'''

from ..Helpers import Tuttifrutti
import copy

class AbstractPattern(object):
    '''
    Provides an abstract class for `Pattern` objects.


    Parameters
    ----------
    Layer: int, optional
        Specifies the `Layer` attribute of the pattern.
        Defaults to None.
    DataType: int, optional
        Specifies the `DataType` attribute of the pattern.
        Defaults to None.
    RotationAngle: float, optional
        Specifies the `RotationAngle` attribute of the pattern.
        Defaults to None.
    StrokeWidth: float, optional
        Specifies the `StrokeWidth` attribute of the pattern.
        Defaults to None.
    ScaleFactor: float, optional
        Specifies the `ScaleFactor` attribute of the pattern.
        Defaults to None.
    '''
    def __init__(self,**kwargs):

        #: str: specifies the type of the pattern.
        self.Type = 'AbstractPattern'

        #: list of float, x- and y- coordinates of the origin point of the pattern
        self._OriginPoint = [0,0]

        #: :class:`TXLWizard.Patterns.Structure.Structure`, reference to the `Structure` instance containing the current pattern
        self.ParentStructure = None

        #: dict: default attributes that are copied to `self.Attributes` upon instantiation. Specifies the allowed attributes
        self.DefaultAttributes = {
            'Layer':None,
            'DataType':None,
            'RotationAngle':None,
            'StrokeWidth':None,
            'ScaleFactor':None,
        }

        #: dict: attribute values of the current pattern. Default values are copied from `self.DefaultAttributes`
        self.Attributes = copy.copy(self.DefaultAttributes)

        for i in self.Attributes:
            if i in kwargs:
                self.Attributes[i] = kwargs[i]

        if 'ParentStructure' in kwargs:
            self.ParentStructure = kwargs['ParentStructure']




    def _GetSVGAttributesString(self,OverrideSVGAttributes = {}):
        '''
        Generate a string of attributes for an SVG xml element node.
        By default, the `class` attribute is set to ["Pattern"] if the current pattern `self.Type` is not in ['Structure','Array','Reference']

        Parameters
        ----------
        OverrideSVGAttributes: dict, optional
            Dictionary with SVG attributes and values. The key corresponds to the SVG attribute name, the value can be a str or list of str.
            Defaults to {}

        Returns
        -------
        str
           string of attributes for an SVG xml element node

        '''
        SVGAttributes = {
            'style':[],
            'class':[],
            'transform':[]
        }
        if not self.Type in ['Structure','Array','Reference']:
            SVGAttributes['class'].append('Pattern')

        Tuttifrutti.update(SVGAttributes,OverrideSVGAttributes,True)

        SVGAttributesString = ''
        for i in SVGAttributes:
            if len(SVGAttributes[i]):
                SVGAttributesString += i+'="'
                if isinstance(SVGAttributes[i], list):
                    if i == 'style':
                        SVGAttributesString += ';'.join(SVGAttributes[i])
                    else:
                        SVGAttributesString += ' '.join(SVGAttributes[i])
                else:
                    SVGAttributesString += SVGAttributes[i]
                SVGAttributesString += '" '

        return SVGAttributesString

    def GetTXLOutput(self):
        '''
        Generates the TXL output commands for the current pattern.
        Needs to be implemented for each pattern type separately in the corresponding inheriting class.

        Returns
        -------
        str
            TXL output commands
        '''
        pass

    def GetSVGOutput(self):
        '''
        Generates the SVG output xml for the current pattern.
        Needs to be implemented for each pattern type separately in the corresponding inheriting class.

        Returns
        -------
        str
            SVG output xml
        '''
        pass



