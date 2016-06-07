import numpy as np


def GetMicrobridgeCoarse(TXLWriter, BridgeWidth, BridgeLength, BridgeEdgeRadius, PadWidth, PadLength, EtchRadius,
                         Layer=1, FineLayerWidth=1.5, FineCoarseOverlap=0.2, FineLayerYLength=5, NumberOfPoints=1000):
    ID = 'MicrobridgeCoarse_BridgeWidth{BridgeWidth:1.2e}_BridgeLength{BridgeLength:1.2e}_BridgeEdgeRadius{BridgeEdgeRadius:1.2e}_PadWidth{PadWidth:1.2e}_PadLength{PadLength:1.2e}_EtchRadius{EtchRadius:1.2e}'.format(
        BridgeWidth=BridgeWidth,
        BridgeLength=BridgeLength,
        BridgeEdgeRadius=BridgeEdgeRadius,
        PadWidth=PadWidth,
        PadLength=PadLength,
        EtchRadius=EtchRadius
    )
    Microbridge = TXLWriter.AddDefinitionStructure(
        ID,
        Layer=Layer)

    PolygonPoints = []

    # Along Bridge
    for x in np.linspace(0, 1. * BridgeLength / 2. - FineLayerWidth + FineCoarseOverlap, 2):
        PolygonPoints.append([
            x,
            1. * BridgeWidth / 2. + FineLayerWidth - FineCoarseOverlap
        ])

    # Ecke
    for y in np.linspace(1. * BridgeWidth / 2. + FineLayerWidth - FineCoarseOverlap,
                         FineLayerYLength - FineCoarseOverlap, 2):
        PolygonPoints.append([
            1. * BridgeLength / 2. - FineLayerWidth + FineCoarseOverlap,
            y
        ])

    # Go to Pad
    for x in np.linspace(1. * BridgeLength / 2. - FineLayerWidth + FineCoarseOverlap, 1. * BridgeLength / 2., 2):
        PolygonPoints.append([
            x,
            FineLayerYLength - FineCoarseOverlap
        ])

    # Along PadY
    for y in np.linspace(1. * BridgeWidth / 2. + 2 * FineLayerWidth - 2 * FineCoarseOverlap, 1. * PadWidth / 2., 2):
        PolygonPoints.append([
            1. * BridgeLength / 2.,
            y
        ])

    # Along PadX
    for x in np.linspace(1. * BridgeLength / 2., 1. * PadLength - EtchRadius, 2):
        PolygonPoints.append([
            1. * BridgeLength / 2.,
            y
        ])

    # Etch Corner
    EtchCornerCenter = [
        1. * BridgeLength / 2. + 1. * PadLength,
        1. * PadWidth / 2. + EtchRadius
    ]
    for Angle in np.linspace(-np.pi / 2., np.pi / 2., NumberOfPoints / 10):
        PolygonPoints.append([
            EtchCornerCenter[0] + EtchRadius * np.cos(Angle),
            EtchCornerCenter[1] + EtchRadius * np.sin(Angle),
        ])

    # Along PadX
    for x in np.linspace(1. * PadLength, 0, 2):
        PolygonPoints.append([
            x,
            1. * PadWidth / 2. + 2 * EtchRadius
        ])

    # Mirror at y-Axis
    OldLength = len(PolygonPoints)
    for i in range(OldLength):
        i2 = OldLength - 1 - i
        PolygonPoints.append([
            -1. * PolygonPoints[i2][0],
            PolygonPoints[i2][1]
        ])

    Microbridge.AddPattern('Polygon', Points=PolygonPoints)

    # Mirror at y-Axis

    PolygonPointsMirroredY = []
    for i in range(len(PolygonPoints)):
        PolygonPointsMirroredY.append([
            PolygonPoints[i][0],
            -1. * PolygonPoints[i][1]
        ])

    Microbridge.AddPattern('Polygon', Points=PolygonPointsMirroredY)

    return Microbridge


def GetMicrobridgeFine(TXLWriter, BridgeWidth, BridgeLength, BridgeEdgeRadius, PadWidth, PadLength, EtchRadius, Layer=1,
                       FineLayerWidth=1.5, FineCoarseOverlap=0.2, FineLayerYLength=5, NumberOfPoints=1000):
    ID = 'MicrobridgeFine_BridgeWidth{BridgeWidth:1.2e}_BridgeLength{BridgeLength:1.2e}_BridgeEdgeRadius{BridgeEdgeRadius:1.2e}_PadWidth{PadWidth:1.2e}_PadLength{PadLength:1.2e}_EtchRadius{EtchRadius:1.2e}'.format(
        BridgeWidth=BridgeWidth,
        BridgeLength=BridgeLength,
        BridgeEdgeRadius=BridgeEdgeRadius,
        PadWidth=PadWidth,
        PadLength=PadLength,
        EtchRadius=EtchRadius
    )
    Microbridge = TXLWriter.AddDefinitionStructure(
        ID,
        Layer=Layer)

    PolygonPoints = []

    # Along Bridge
    for x in np.linspace(0, 1. * BridgeLength / 2. - BridgeEdgeRadius, 2):
        PolygonPoints.append([
            x,
            1. * BridgeWidth / 2.
        ])

    # Bridge Edge
    BridgeEdgeCenter = [
        1. * BridgeLength / 2. - 1. * BridgeEdgeRadius,
        1. * BridgeWidth / 2. + 1. * BridgeEdgeRadius
    ]
    for Angle in np.linspace(-np.pi / 2., 0, NumberOfPoints / 10):
        PolygonPoints.append([
            BridgeEdgeCenter[0] + BridgeEdgeRadius * np.cos(Angle),
            BridgeEdgeCenter[1] + BridgeEdgeRadius * np.sin(Angle),
        ])

    # Along PadY
    for y in np.linspace(BridgeEdgeRadius, FineLayerYLength, 2):
        PolygonPoints.append([
            1. * BridgeLength / 2.,
            y
        ])

    # Ecke
    for x in np.linspace(1. * BridgeLength / 2., 1. * BridgeLength / 2. - FineLayerWidth, 2):
        PolygonPoints.append([
            x,
            FineLayerYLength
        ])

    # Ecke
    for y in np.linspace(BridgeEdgeRadius + FineLayerYLength, 1. * BridgeWidth / 2. + FineLayerWidth, 2):
        PolygonPoints.append([
            1. * BridgeLength / 2. - FineLayerWidth,
            y
        ])

    # Back to center
    PolygonPoints.append([
        0,
        1. * BridgeWidth / 2. + FineLayerWidth
    ])

    # Mirror at y-Axis
    OldLength = len(PolygonPoints)
    for i in range(OldLength):
        i2 = OldLength - 1 - i
        PolygonPoints.append([
            -1. * PolygonPoints[i2][0],
            PolygonPoints[i2][1]
        ])

    Microbridge.AddPattern('Polygon', Points=PolygonPoints)

    # Mirror at y-Axis

    PolygonPointsMirroredY = []
    for i in range(len(PolygonPoints)):
        PolygonPointsMirroredY.append([
            PolygonPoints[i][0],
            -1. * PolygonPoints[i][1]
        ])

    Microbridge.AddPattern('Polygon', Points=PolygonPointsMirroredY)

    return Microbridge
