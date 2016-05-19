'''
Implements a class for `Structure` objects (`STRUCT`).\n
A `Structure` is a container for `Pattern` objects.
'''

from . import AbstractPattern
from ..Helpers import Tuttifrutti
import copy
import importlib


class Structure(AbstractPattern.AbstractPattern):
    '''
    Implements a class for `Structure` objects.\n
    Corresponds to the TXL command `STRUCT`.\n
    A `Structure` is a container for `Pattern` objects.

    Parameters
    ---------
    ID: str
        Unique identification of the structure. Also used when referencing to this structure.
    TXLOutput: bool, optional
        If set to False, the TXL Output is suppressed.
        Defaults to True
    **kwargs
        keyword arguments passed to the :class:`TXLWizard.Patterns.AbstractPattern.AbstractPattern` constructor.
        Can specify attributes of the current pattern.
    '''

    def __init__(self, ID, **kwargs):
        super(Structure, self).__init__(**kwargs)

        #: str: specifies the type of the pattern. Set to 'Structure'
        self.Type = 'Structure'

        #: str: Unique identification of the structure. Also used when referencing to this structure.
        self.ID = ID

        #: list of :class:`TXLWizard.Patterns.AbstractPattern.AbstractPattern`: Patterns that are contained in this structure
        self.Patterns = []

        #: bool: If set to False, the TXL Output is suppressed.
        self.TXLOutput = True

        #: dict: attribute values of the next pattern to be added. Default values are copied from `self.DefaultAttributes`
        self.CurrentAttributes = copy.copy(self.DefaultAttributes)

        for i in self.CurrentAttributes:
            if i in kwargs:
                self.CurrentAttributes[i] = kwargs[i]

        if 'TXLOutput' in kwargs:
            self.TXLOutput = kwargs['TXLOutput']

    def AddPattern(self, PatternType, **kwargs):
        '''
        Adds a `Pattern` of type `PatternType` to the structure.
        Creates an instance of `TXLWizard.Patterns.{PatternType}.{PatternType}`.
        The `kwargs` are passed to the corresponding constructor and allow specifying
        pattern parameters as defined in the constructor of the corresponding pattern class
        and attributes as defined in :class:`TXLWizard.Patterns.AbstractPattern.AbstractPattern`.

        Parameters
        ----------
        PatternType: {'Array', 'Circle', 'Ellipse', 'Polygon', 'Polyline', 'Reference'}
            Type of the pattern to be added.
        **kwargs
            keyword arguments are passed to the corresponding constructor and allow specifying
            pattern parameters as defined in the constructor of the corresponding pattern class
            and attributes as defined in :class:`TXLWizard.Patterns.AbstractPattern.AbstractPattern`.

        Returns
        -------
        :class:`TXLWizard.Patterns.{PatternType}.{PatternType}`
            returns the created pattern object
        '''

        f = importlib.import_module('.' + PatternType, __package__)
        class_ = getattr(f, PatternType)
        kwargs['ParentStructure'] = self
        for i in self.CurrentAttributes:
            if i in kwargs:
                self.CurrentAttributes[i] = kwargs[i]
            elif self.CurrentAttributes[i] != None:
                kwargs[i] = self.CurrentAttributes[i]

        Pattern = class_(**kwargs)
        self.Patterns.append(Pattern)
        return Pattern

    def GetTXLOutput(self):
        CurrentAttributes = copy.copy(self.DefaultAttributes)
        TXL = ''
        TXL += 'STRUCT ' + self.ID + '\n'
        # TXL += self._GetAttributesTXL(CurrentAttributes)
        for i in self.Patterns:
            NewCurrentAttributes = copy.copy(self.DefaultAttributes)
            AttributesChanged = False
            for j in i.Attributes:
                if i.Attributes[j] != None and CurrentAttributes[j] != i.Attributes[j]:
                    NewCurrentAttributes[j] = i.Attributes[j]
                    AttributesChanged = True
                elif CurrentAttributes[j] != None:
                    NewCurrentAttributes[j] = CurrentAttributes[j]
            CurrentAttributes = NewCurrentAttributes
            if AttributesChanged:
                TXL += self._GetAttributesTXL(CurrentAttributes)
            TXL += i.GetTXLOutput()
        TXL += 'ENDSTRUCT' + '\n\n'
        return TXL

    def _GetAttributesTXL(self, Attributes):
        '''
        Generates the TXL commands for the attributes given in `Attributes`

        Parameters
        ----------
        Attributes: dict
            Dictionary with attributes and their values.

        Returns
        -------
        str
            TXL commands for the attributes specified

        '''
        AttributeMapping = {
            'Layer': 'LAYER {:d}',
            'DataType': 'DATATYPE {:d}',
            'RotationAngle': 'ANGLE {:1.2f}',
            'StrokeWidth': 'WIDTH {:1.4f}',
            'ScaleFactor': 'MAG {:1.4f}'
        }
        TXL = ''
        for i in Attributes:
            if Attributes[i] != None:
                TXL += AttributeMapping[i].format(Attributes[i]) + '\n'
        return TXL

    def GetSVGOutput(self):
        CurrentAttributes = copy.copy(self.DefaultAttributes)
        SVG = ''
        SVG += '<g id="' + self.ID.replace('+', '') + '" ' + self._GetSVGAttributesString() + '>' + '\n'

        for i in self.Patterns:
            NewCurrentAttributes = copy.copy(self.DefaultAttributes)
            for j in i.Attributes:
                if i.Attributes[j] != None and CurrentAttributes[j] != i.Attributes[j]:
                    NewCurrentAttributes[j] = i.Attributes[j]
                elif CurrentAttributes[j] != None:
                    NewCurrentAttributes[j] = CurrentAttributes[j]
            CurrentAttributes = NewCurrentAttributes
            if abs(i._OriginPoint[0]) > 0 or abs(i._OriginPoint[1]) > 0:
                Transforms = ['translate({:1.4f},{:1.4f})'.format(i._OriginPoint[0], i._OriginPoint[1])]
            else:
                Transforms = []

            SVGAttributes = self._GetPatternSVGAttributesString(i.Type, CurrentAttributes, {
                'transform': Transforms
            })

            SVG += ('' +
                    '<g ' + SVGAttributes + '>' + '\n' +
                    '    ' + i.GetSVGOutput() +
                    '</g>' + '\n')
        SVG += '</g>' + '\n'
        return SVG

    def _GetPatternSVGAttributesString(self, PatternType, Attributes, OverrideSVGAttributes={}):
        '''
        Generate SVG attributes according to the `PatternType` and `Attributes` specified.
        SVG attributes can also be overridden or added with `OverrideSVGAttributes`

        Parameters
        ----------
        PatternType: str
            Type of the pattern
        Attributes: dict
            Attributes of the pattern
        OverrideSVGAttributes: dict
            Dictionary with SVG attributes that will be added or overridden.

        Returns
        -------
        str
            SVG attributes
        '''
        SVGAttributes = {
            'style': [],
            'class': [],
            'transform': []
        }
        Tuttifrutti.update(SVGAttributes, OverrideSVGAttributes, True)

        for i in Attributes:
            if Attributes[i] != None:
                if i == 'Layer':
                    SVGAttributes['class'].append('Layer{:d}'.format(Attributes[i]))
                elif i == 'RotationAngle' and PatternType in ['Reference']:
                    SVGAttributes['transform'].append('rotate({:1.4f})'.format(Attributes[i]))
                elif i == 'ScaleFactor' and PatternType in ['Reference']:
                    SVGAttributes['transform'].append('scale({:1.4f})'.format(Attributes[i]))
                    # if i == 'StrokeWidth' and False:
                    #    SVGAttributes['style'].append('stroke-width: {:1.4f}'.format(Attributes[i]))

        return super(Structure, self)._GetSVGAttributesString(SVGAttributes)
