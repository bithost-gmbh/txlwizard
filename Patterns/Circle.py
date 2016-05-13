from . import AbstractPattern
import math
class Circle(AbstractPattern.AbstractPattern):
    def __init__(self,Center,Radius,**kwargs):
        super(Circle, self).__init__(**kwargs)
        self.Type = 'Circle'
        self.OriginPoint = Center

        self.PathOnly = False
        self.Extended = False
        self.RoundCaps = False
        self.Center = Center
        self.Radius = Radius
        self.StartAngle = None
        self.EndAngle = None
        self.NumberOfPoints = None
        for i in ['PathOnly','StartAngle','EndAngle','NumberOfPoints','Extended','PathOnly','RoundCaps']:
            if i in kwargs:
                setattr(self,i,kwargs[i])

        if self.StartAngle != None and self.EndAngle != None:
            self.StartPoint = [math.cos(self.StartAngle/360.*2.*math.pi)*self.Radius,math.sin(self.StartAngle/360.*2.*math.pi)*self.Radius]
            self.EndPoint = [math.cos(self.EndAngle/360.*2.*math.pi)*self.Radius,math.sin(self.EndAngle/360.*2.*math.pi)*self.Radius]


    def GetTXLOutput(self):
        BoundaryString = ''
        BoundaryStringEnd = ''
        if self.PathOnly:
            BoundaryString = 'P'
            BoundaryStringEnd = BoundaryString
            if self.RoundCaps:
                BoundaryString += 'R'
            elif self.Extended:
                BoundaryString += 'E'
        TXL = ''
        TXL += 'C'+BoundaryString+' '
        TXL += '{:1.4f} {:1.4f},{:1.4f} '.format(self.Radius,self.Center[0],self.Center[1])
        if self.StartAngle != None and self.EndAngle != None:
            if not self.PathOnly:
                TXL += '('
            TXL += '{:1.4f} {:1.4f} '.format(self.StartAngle,self.EndAngle)

            if self.NumberOfPoints != None:
                TXL += '{:d}'.format(self.NumberOfPoints)

            if not self.PathOnly:
                TXL += ') '

        TXL += 'ENDC'+BoundaryStringEnd+'\n'
        return TXL


    def GetSVGOutput(self):
        SVG = ''
        if self.StartAngle == None or abs(self.EndAngle-self.StartAngle)==360:
            SVGAttributes = {
                #'cx':'{:1.4f}'.format(self.Center[0]),
                #'cy':'{:1.4f}'.format(self.Center[1]),
                'cx':'0',
                'cy':'0',
                'r':'{:1.4f}'.format(self.Radius),
            }
            if self.PathOnly:
                SVGAttributes['style'] = ['fill:none','stroke-width:{:1.4f}'.format(self.Attributes['StrokeWidth'])]
            SVG += ('<circle '+self.GetSVGAttributesString(SVGAttributes)+
                   ' />'+'\n')
        else:
            LargeAngle = 0
            if abs(self.EndAngle-self.StartAngle)>=180:
                LargeAngle = 1
            # See http://www.w3.org/TR/2003/REC-SVG11-20030114/paths.html#PathDataEllipticalArcCommands
            SweepFlag = 1
            SVGAttributes = {
                'd':'m {:1.4f} {:1.4f} '.format(self.StartPoint[0], self.StartPoint[1])+
                    #'l {:1.4f} {:1.4f} '.format(StartPoint[0], StartPoint[1])+
                    'a {:1.4f} {:1.4f} 0 {:d} {:d} {:1.4f} {:1.4f} '.format(self.Radius,self.Radius,LargeAngle,SweepFlag,self.EndPoint[0]-self.StartPoint[0],self.EndPoint[1]-self.StartPoint[1])
                    #'l {:1.4f} {:1.4f}'.format(self.Center[0],self.Center[1])
            }
            if self.PathOnly:
                SVGAttributes['style'] = ['fill:none','stroke-width:{:1.4f}'.format(self.Attributes['StrokeWidth'])]
                if self.RoundCaps:
                    SVGAttributes['stroke-linecap'] = 'round'
                elif self.Extended:
                    SVGAttributes['stroke-linecap'] = 'square'

            SVG += ('<path '+self.GetSVGAttributesString(SVGAttributes)+' />')
        return SVG