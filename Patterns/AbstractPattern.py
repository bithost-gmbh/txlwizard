from ..Helpers import Tuttifrutti
import copy
class AbstractPattern(object):
    def __init__(self,**kwargs):
        self.Type = 'AbstractPattern'
        self.OriginPoint = [0,0]
        self.ParentStructure = None

        self.DefaultAttributes = {
            'Layer':None,
            'DataType':None,
            'RotationAngle':None,
            'StrokeWidth':None,
            'ScaleFactor':None,
        }
        self.Attributes = copy.copy(self.DefaultAttributes)

        for i in self.Attributes:
            if i in kwargs:
                self.Attributes[i] = kwargs[i]

        if 'ParentStructure' in kwargs:
            self.ParentStructure = kwargs['ParentStructure']




    def GetSVGAttributesString(self,OverrideSVGAttributes = {}):
        SVGAttributes = {
            'style':[],
            'class':[],
            'transform':[]
        }
        if not self.Type in ['Structure','Array','Reference']:
            SVGAttributes['class'].append('Pattern')
        #SVGAttributes['class'].append(self.Type)
        #SVGAttributes['class'].append('Object')

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
        pass

    def GetSVGOutput(self):
        pass


