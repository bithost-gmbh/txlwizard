import numpy as np
def GetCornerCube(TXLWriter, ParabolaFocus, XCutoff, AirGapX, AirGapY, NumberOfPoints = 1000, Layer=1):
    ID = 'CornerCube_Focus{ParabolaFocus:1.2e}_Cutoff{XCutoff:1.2e}_GapX{AirGapX:1.2e}_GapY{AirGapY:1.2e}'.format(ParabolaFocus=ParabolaFocus,
                                                            XCutoff=XCutoff,
                                                            AirGapX=AirGapX,
                                                            AirGapY=AirGapY
      )
    CornerCube = TXLWriter.AddDefinitionStructure(
            ID, Layer=Layer)
    PolygonPoints = []

    # Parabola
    for x in np.linspace(2*ParabolaFocus,XCutoff,NumberOfPoints):
        PolygonPoints.append([
            x,
            MirrorParabola(ParabolaFocus,x)
        ])


    # Corner Circle
    TangentAngleAtXCutoff = np.arctan(MirrorParabolaDerivative(ParabolaFocus,XCutoff))
    NormalAngleAtXCutoff = TangentAngleAtXCutoff+np.pi/2
    CornerCircleCenterXOffset = -1.*AirGapY*np.sin(TangentAngleAtXCutoff)/2.
    CornerCircleCenterYOffset = 1.*AirGapY*np.cos(TangentAngleAtXCutoff)/2.
    CornerCircleCenter = [
        XCutoff+CornerCircleCenterXOffset,
        MirrorParabola(ParabolaFocus,XCutoff)+CornerCircleCenterYOffset
    ]
    CornerCircleRadius = 1.*AirGapY/2.
    CornerCircleStartAngle = TangentAngleAtXCutoff-np.pi/2
    CornerCircleEndAngle = CornerCircleStartAngle-np.pi-TangentAngleAtXCutoff
    for Angle in np.linspace(CornerCircleStartAngle,CornerCircleEndAngle,NumberOfPoints/2):
        PolygonPoints.append([
            CornerCircleCenter[0]+CornerCircleRadius*np.cos(Angle),
            CornerCircleCenter[1]+CornerCircleRadius*np.sin(Angle)
        ])

    # Ellipse
    for x in np.linspace(XCutoff+CornerCircleCenterXOffset,2.*ParabolaFocus+AirGapX,NumberOfPoints):
        PolygonPoints.append([
            x,
            MirrorEllipse(
                2.*ParabolaFocus-XCutoff+AirGapX-CornerCircleCenterXOffset,
                MirrorParabola(ParabolaFocus,XCutoff)+CornerCircleCenterYOffset+AirGapY/2.,
                x-XCutoff-CornerCircleCenterXOffset
            )
        ])

    # Mirror at x-Axis
    OldLength = len(PolygonPoints)
    for i in range(OldLength):
        i2 = OldLength-1-i
        PolygonPoints.append([
            PolygonPoints[i2][0],
            -1.*PolygonPoints[i2][1]
        ])

    CornerCube.AddPattern('Polygon',Points = PolygonPoints)
    return CornerCube



def MirrorParabola(f,x):
    return ((2.*f)**2-x**2)/(4.*f)

def MirrorParabolaDerivative(f,x):
    return (-x)/(2.*f)

def MirrorEllipse(a,b,x):
    return 1.*b/a*np.sqrt(a**2-x**2)