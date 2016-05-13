import numpy as np
def GetMarkers(TXLWriter, Size=10, OffsetSmall=750, OffsetLarge = 1500, Layer = 1):
    MarkerSingle = TXLWriter.AddDefinitionStructure(
            'MarkerSingle', Layer = Layer)
    PolygonPoints = []

    # Large
    PolygonPoints.append([
        -1.*Size/2.,
        -1.*Size/2.,
    ])
    PolygonPoints.append([
        1.*Size/2.,
        -1.*Size/2.,
    ])
    PolygonPoints.append([
        1.*Size/2.,
        1.*Size/2.,
    ])
    PolygonPoints.append([
        -1.*Size/2.,
        1.*Size/2.,
    ])
    MarkerSingle.AddPattern('Polygon',Points = PolygonPoints)

    ID = 'Markers'
    Markers = TXLWriter.AddContentStructure(
            ID, Layer = Layer)

    # Small
    for i in [[-1,0],[0,1],[1,0],[0,-1]]:
        PolygonPoints = []
        XOffset = i[0]*OffsetSmall
        YOffset = i[1]*OffsetSmall

        PolygonPoints.append([
            XOffset-1.*Size/2.,
            YOffset-1.*Size/2.,
        ])
        PolygonPoints.append([
            XOffset+1.*Size/2.,
            YOffset-1.*Size/2.,
        ])
        PolygonPoints.append([
            XOffset+1.*Size/2.,
            YOffset+1.*Size/2.,
        ])
        PolygonPoints.append([
            XOffset-1.*Size/2.,
            YOffset+1.*Size/2.,
        ])
        Markers.AddPattern('Polygon',Points = PolygonPoints)



    MarkersContent = TXLWriter.AddContentStructure(ID+'Content')
    MarkersContent.AddPattern('Reference',ReferencedStructureID = Markers.ID,OriginPoint = [0,0])

    return MarkersContent


