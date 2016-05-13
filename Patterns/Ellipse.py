from . import AbstractPattern
import math
class Ellipse(AbstractPattern.AbstractPattern):
    def __init__(self, Center, RadiusX, RadiusY, **kwargs):
        super(Ellipse, self).__init__(**kwargs)
        self.Type = 'Ellipse'
        self.OriginPoint = Center

        self.PathOnly = False
        self.Center = Center
        self.RadiusX = RadiusX
        self.RadiusY = RadiusY

        self.StartAngle = 0
        self.EndAngle = 360
        self.NumberOfPoints = None
        for i in ['PathOnly','StartAngle','EndAngle','NumberOfPoints']:
            if i in kwargs:
                setattr(self,i,kwargs[i])

        if self.StartAngle != None and self.EndAngle != None:
            self.StartPoint = [math.cos(self.StartAngle/360.*2.*math.pi)*self.RadiusX,math.sin(self.StartAngle/360.*2.*math.pi)*self.RadiusY]
            self.EndPoint = [math.cos(self.EndAngle/360.*2.*math.pi)*self.RadiusX,math.sin(self.EndAngle/360.*2.*math.pi)*self.RadiusY]



    def GetTXLOutput(self):

        TXL = ''
        TXL += 'ELP '
        TXL += '{:1.4f} {:1.4f} {:1.4f},{:1.4f} '.format(self.RadiusX, self.RadiusY,self.StartPoint[0],self.StartPoint[1])
        if self.StartAngle != None and self.EndAngle != None:
            if not self.PathOnly:
                TXL += '('
            TXL += '{:1.4f} {:1.4f} '.format(self.StartAngle,self.EndAngle)

            if self.NumberOfPoints != None:
                TXL += '{:d}'.format(self.NumberOfPoints)

            if not self.PathOnly:
                TXL += ')'

        TXL += 'ENDELP'+'\n'
        return TXL


    def GetSVGOutput(self):

        SVG = ''
        if self.StartAngle == None or abs(self.EndAngle-self.StartAngle)==360:
            SVG += ('<ellipse '+self.GetSVGAttributesString({
                            #'cx':'{:1.4f}'.format(self.Center[0]),
                            #'cy':'{:1.4f}'.format(self.Center[1]),
                            'cx':'0',
                            'cy':'0',
                            'rx':'{:1.4f}'.format(self.RadiusX),
                            'ry':'{:1.4f}'.format(self.RadiusY),
                        })+
                   ' />'+'\n')
        else:
            # See http://www.w3.org/TR/2003/REC-SVG11-20030114/paths.html#PathDataEllipticalArcCommands
            LargeAngle = 0
            if abs(self.EndAngle-self.StartAngle)>=180:
                LargeAngle = 1
            SVG += ('<path '+self.GetSVGAttributesString({
                'd':'m {:1.4f} {:1.4f} '.format(self.StartPoint[0], self.StartPoint[1])+
                    #'l {:1.4f} {:1.4f} '.format(self.StartPoint[0], self.StartPoint[1])+
                    'a {:1.4f} {:1.4f} 0 0 {:d} {:1.4f} {:1.4f} '.format(self.RadiusX,self.RadiusY,LargeAngle,self.EndPoint[0]-self.StartPoint[0],self.EndPoint[1]-self.StartPoint[1])
                    #'l {:1.4f} {:1.4f}'.format(self.Center[0],self.Center[1])
            })+' />')
        return SVG