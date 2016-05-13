from . import AbstractPattern
from ..Helpers import Tuttifrutti
import copy
import importlib

class Structure(AbstractPattern.AbstractPattern):
    def __init__(self,ID,**kwargs):
        super(Structure, self).__init__(**kwargs)
        self.Type = 'Structure'

        self.ID = ID
        self.Patterns = []
        self.TXLOutput = True

        self.CurrentAttributes = copy.copy(self.DefaultAttributes)
        for i in self.CurrentAttributes:
            if i in kwargs:
                self.CurrentAttributes[i] = kwargs[i]

        if 'TXLOutput' in kwargs:
            self.TXLOutput = kwargs['TXLOutput']

    def AddPattern(self,PatternType,**kwargs):
        f = importlib.import_module('.'+PatternType,__package__)
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
        TXL += 'STRUCT '+self.ID+'\n'
        #TXL += self.GetAttributesTXL(CurrentAttributes)
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
                TXL += self.GetAttributesTXL(CurrentAttributes)
            TXL += i.GetTXLOutput()
        TXL += 'ENDSTRUCT'+'\n\n'
        return TXL

    def GetAttributesTXL(self,Attributes):
        AttributeMapping = {
            'Layer':'LAYER {:d}',
            'DataType':'DATATYPE {:d}',
            'RotationAngle':'ANGLE {:1.2f}',
            'StrokeWidth':'WIDTH {:1.4f}',
            'ScaleFactor':'MAG {:1.4f}'
        }
        TXL = ''
        for i in Attributes:
            if Attributes[i] != None:
                TXL += AttributeMapping[i].format(Attributes[i])+'\n'
        return TXL

    def GetSVGOutput(self):
        CurrentAttributes = copy.copy(self.DefaultAttributes)
        SVG = ''
        SVG += '<g id="'+self.ID.replace('+','')+'" '+self.GetSVGAttributesString()+'>'+'\n'

        for i in self.Patterns:
            NewCurrentAttributes = copy.copy(self.DefaultAttributes)
            for j in i.Attributes:
                if i.Attributes[j] != None and CurrentAttributes[j] != i.Attributes[j]:
                    NewCurrentAttributes[j] = i.Attributes[j]
                elif CurrentAttributes[j] != None:
                    NewCurrentAttributes[j] = CurrentAttributes[j]
            CurrentAttributes = NewCurrentAttributes
            if abs(i.OriginPoint[0]) > 0 or abs(i.OriginPoint[1])>0:
                Transforms = ['translate({:1.4f},{:1.4f})'.format(i.OriginPoint[0],i.OriginPoint[1])]
            else:
                Transforms = []

            SVGAttributes = self.GetPatternSVGAttributesString(i.Type,CurrentAttributes,{
                        'transform':Transforms
                    })

            SVG += (''+
                    '<g '+SVGAttributes+'>'+'\n'+
                        '    '+i.GetSVGOutput()+
                    '</g>'+'\n')
        SVG += '</g>'+'\n'
        return SVG

    def GetPatternSVGAttributesString(self,PatternType,Attributes, OverrideSVGAttributes = {}):
        SVGAttributes = {
            'style':[],
            'class':[],
            'transform':[]
        }
        Tuttifrutti.update(SVGAttributes,OverrideSVGAttributes,True)

        for i in Attributes:
            if Attributes[i] != None:
                if i == 'Layer':
                    SVGAttributes['class'].append('Layer{:d}'.format(Attributes[i]))
                elif i == 'RotationAngle' and PatternType in ['Reference']:
                    SVGAttributes['transform'].append('rotate({:1.4f})'.format(Attributes[i]))
                elif i == 'ScaleFactor' and PatternType in ['Reference']:
                    SVGAttributes['transform'].append('scale({:1.4f})'.format(Attributes[i]))
                #if i == 'StrokeWidth' and False:
                #    SVGAttributes['style'].append('stroke-width: {:1.4f}'.format(Attributes[i]))

        return super(Structure,self).GetSVGAttributesString(SVGAttributes)