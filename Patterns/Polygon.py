from . import AbstractPattern
class Polygon(AbstractPattern.AbstractPattern):
    def __init__(self,Points,**kwargs):
        super(Polygon, self).__init__(**kwargs)
        self.Type = 'Polygon'
        self.Points = Points
        self.OriginPoint = [0,0]
        self.RoundCaps = False

        self.PathOnly = False

        for i in ['PathOnly','RoundCaps']:
            if i in kwargs:
                setattr(self,i,kwargs[i])


    def GetTXLOutput(self):
        if self.PathOnly:
            CommandString = 'P'
            EndCommandString = CommandString
            if self.RoundCaps:
                CommandString += 'R'
        else:
            CommandString = 'B'
            EndCommandString = CommandString
        TXL = ''
        TXL += CommandString+' '
        for Point in self.Points:
            TXL += '{:1.4f},{:1.4f} '.format(Point[0],Point[1])
        TXL += 'END'+EndCommandString+'\n'
        return TXL


    def GetSVGOutput(self):
        SVG = ''

        PointsString = ''
        for Point in self.Points:
            PointsString += '{:1.4f},{:1.4f} '.format(Point[0],Point[1])
        SVGAttributes = {'points':PointsString}
        if self.PathOnly:
            SVGAttributes['style'] = ['fill:none','stroke-width:{:1.4f}'.format(self.Attributes['StrokeWidth'])]
            if self.RoundCaps:
                SVGAttributes['stroke-linecap'] = 'round'
            SVG += '<polyline '+self.GetSVGAttributesString(SVGAttributes)+' />'+'\n'
        else:
            SVG += '<polygon '+self.GetSVGAttributesString(SVGAttributes)+' />'+'\n'




        return SVG