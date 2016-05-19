'''
Add squares to `TXLWriter` that can be used as alignment markers.
'''


def GetAlignmentMarkers(TXLWriter, Size=10, OffsetSmall=750, OffsetLarge=1500, Layer=1):
    '''
    Add squares that can be used as alignment markers

    Parameters
    ----------
    TXLWriter: :class:`TXLWizard.TXLWriter.TXLWriter`
        Current Instance of :class:`TXLWizard.TXLWriter.TXLWriter`
    Size: float, optional
        Size of the markers.
        Defaults to 10
    OffsetSmall: float, optional
        first offset from center.
        Defaults to 750
    OffsetLarge: float, optional
        second offset from center.
        Defaults to 1500
    Layer: int, optional
        Layer the pattern should be rendered in.
        Defaults to 1

    Returns
    -------
    :class:`TXLWizard.Patterns.Structure.Structure`
        `Structure` object containing the patterns representing the alignment markers
    '''

    ID = 'Markers'
    Markers = TXLWriter.AddContentStructure(
        ID, Layer=Layer)

    for Offset in [OffsetSmall, OffsetLarge]:
        for i in [[-1, 0], [0, 1], [1, 0], [0, -1]]:
            PolygonPoints = []
            XOffset = i[0] * OffsetSmall
            YOffset = i[1] * OffsetSmall

            PolygonPoints.append([
                XOffset - 1. * Size / 2.,
                YOffset - 1. * Size / 2.,
            ])
            PolygonPoints.append([
                XOffset + 1. * Size / 2.,
                YOffset - 1. * Size / 2.,
            ])
            PolygonPoints.append([
                XOffset + 1. * Size / 2.,
                YOffset + 1. * Size / 2.,
            ])
            PolygonPoints.append([
                XOffset - 1. * Size / 2.,
                YOffset + 1. * Size / 2.,
            ])
            Markers.AddPattern('Polygon', Points=PolygonPoints)

    return Markers
