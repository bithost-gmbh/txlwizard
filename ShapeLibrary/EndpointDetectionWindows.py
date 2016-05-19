'''
Module `TXLWizard.ShapeLibrary.EndpointDetectionWindows` contains the function `GetEndpointDetectionWindows`
'''


def GetEndpointDetectionWindows(TXLWriter, SizeLarge=1000, SizeSmall=750, Offset=1500, Layer=1):
    '''
    Add five squares that can be used as endpoint detection windows.
    The first square of size `SizeLarge` will be placed in the center.
    The second to fifth square of size `SizeSmall` will be placed at x / y = +-`Offset` / +-`Offset`

    Parameters
    ----------
    TXLWriter: :class:`TXLWizard.TXLWriter.TXLWriter`
        Current Instance of :class:`TXLWizard.TXLWriter.TXLWriter`
    SizeLarge: float, optional
        Size of the center square.
        Defaults to 1000
    SizeSmall: float, optional
        Size of the four peripheral square.
        Defaults to 750
    Offset: float, optional
        Offset of the peripheral squares to the center.
        Defaults to 1500
    Layer: int, optional
        Layer the pattern should be rendered in.
        Defaults to 1

    Returns
    -------
    :class:`TXLWizard.Patterns.Structure.Structure`
        `Structure` object containing the patterns representing the endpoint detection windows
    '''
    ID = 'EndpointDetectionWindows'
    EndpointDetectionWindows = TXLWriter.AddDefinitionStructure(
        ID, Layer=Layer)
    PolygonPoints = []

    # Large
    PolygonPoints.append([
        -1. * SizeLarge / 2.,
        -1. * SizeLarge / 2.,
    ])
    PolygonPoints.append([
        1. * SizeLarge / 2.,
        -1. * SizeLarge / 2.,
    ])
    PolygonPoints.append([
        1. * SizeLarge / 2.,
        1. * SizeLarge / 2.,
    ])
    PolygonPoints.append([
        -1. * SizeLarge / 2.,
        1. * SizeLarge / 2.,
    ])
    EndpointDetectionWindows.AddPattern('Polygon', Points=PolygonPoints)

    # Small
    for i in [[-1, 0], [0, 1], [1, 0], [0, -1]]:
        PolygonPoints = []
        XOffset = i[0] * Offset
        YOffset = i[1] * Offset

        PolygonPoints.append([
            XOffset - 1. * SizeSmall / 2.,
            YOffset - 1. * SizeSmall / 2.,
        ])
        PolygonPoints.append([
            XOffset + 1. * SizeSmall / 2.,
            YOffset - 1. * SizeSmall / 2.,
        ])
        PolygonPoints.append([
            XOffset + 1. * SizeSmall / 2.,
            YOffset + 1. * SizeSmall / 2.,
        ])
        PolygonPoints.append([
            XOffset - 1. * SizeSmall / 2.,
            YOffset + 1. * SizeSmall / 2.,
        ])
        EndpointDetectionWindows.AddPattern('Polygon', Points=PolygonPoints)

    EndpointDetectionWindowsContent = TXLWriter.AddContentStructure(ID + 'Content')
    EndpointDetectionWindowsContent.AddPattern('Reference', ReferencedStructureID=EndpointDetectionWindows.ID,
                                               OriginPoint=[0, 0])

    return EndpointDetectionWindowsContent
