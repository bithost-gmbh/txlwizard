import numpy as np
def GetEndpointDetectionWindows(TXLWriter, SizeLarge=1000, SizeSmall=750, Offset = 1500, Layer = 1):
    ID = 'EndpointDetectionWindows'
    EndpointDetectionWindows = TXLWriter.AddDefinitionStructure(
            ID, Layer = Layer)
    PolygonPoints = []

    # Large
    PolygonPoints.append([
        -1.*SizeLarge/2.,
        -1.*SizeLarge/2.,
    ])
    PolygonPoints.append([
        1.*SizeLarge/2.,
        -1.*SizeLarge/2.,
    ])
    PolygonPoints.append([
        1.*SizeLarge/2.,
        1.*SizeLarge/2.,
    ])
    PolygonPoints.append([
        -1.*SizeLarge/2.,
        1.*SizeLarge/2.,
    ])
    EndpointDetectionWindows.AddPattern('Polygon',Points = PolygonPoints)

    # Small
    for i in [[-1,0],[0,1],[1,0],[0,-1]]:
        PolygonPoints = []
        XOffset = i[0]*Offset
        YOffset = i[1]*Offset

        PolygonPoints.append([
            XOffset-1.*SizeSmall/2.,
            YOffset-1.*SizeSmall/2.,
        ])
        PolygonPoints.append([
            XOffset+1.*SizeSmall/2.,
            YOffset-1.*SizeSmall/2.,
        ])
        PolygonPoints.append([
            XOffset+1.*SizeSmall/2.,
            YOffset+1.*SizeSmall/2.,
        ])
        PolygonPoints.append([
            XOffset-1.*SizeSmall/2.,
            YOffset+1.*SizeSmall/2.,
        ])
        EndpointDetectionWindows.AddPattern('Polygon',Points = PolygonPoints)


    EndpointDetectionWindowsContent = TXLWriter.AddContentStructure(ID+'Content')
    EndpointDetectionWindowsContent.AddPattern('Reference',ReferencedStructureID = EndpointDetectionWindows.ID,OriginPoint = [0,0])

    return EndpointDetectionWindowsContent


