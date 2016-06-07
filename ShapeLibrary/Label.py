'''
Renders arbitrary text in `TXLWriter`.
'''


def GetLabel(TXLWriter, Text, OriginPoint=[0, 0], FontSize=100, StrokeWidth=10, RotationAngle=0, FillCharacters=True,
             RoundCaps=False, Layer=1, **kwargs):
    '''
    Renders arbitrary text.
    Will have an automatically generated ID.

    Parameters
    ----------
    TXLWriter: :class:`TXLWizard.TXLWriter.TXLWriter`
        Current Instance of :class:`TXLWizard.TXLWriter.TXLWriter`
    Text: str
        Text to be displayed
    OriginPoint: list of float, optional
        x- and y-coordinates of the origin point of the label.
        Defaults to [0,0]
    FontSize: float, optional
        Font size. Character height = font size.
        Defaults to 100
    StrokeWidth: float
        line thickness of the letters.
        Defaults to 10
    RotationAngle: float
        Angle by which the text is rotated.
        Defaults to 0
    FillCharacters: bool, optional
        If set to True, closed boundaries will be filled.
        Can be useful if there should be no free-standing parts.
        Defaults to True
    RoundCaps: bool, optional
        If set to True, the paths will habe rounded ends. Should be set to False for better e-Beam Performance
        Defaults to False.
    Layer: int, optional
        Layer the text should be rendered in.
        Defaults to 1
    **kwargs
        keyword arguments

    Returns
    -------
    :class:`TXLWizard.Patterns.Structure.Structure`
        `Structure` object containing the patterns representing the text

    Examples
    --------

    IGNORE:

        >>> import sys
        >>> import os.path
        >>> sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../../'))

    IGNORE

    Import required modules

    >>> import TXLWizard.TXLWriter
    >>> import TXLWizard.ShapeLibrary.Label

    Initialize TXLWriter
    >>> TXLWriter = TXLWizard.TXLWriter.TXLWriter()

    Add a Label

    >>> SampleLabelObject = TXLWizard.ShapeLibrary.Label.GetLabel(
    ...     TXLWriter,
    ...     Text='This is my text',
    ...     OriginPoint=[
    ...         -200, 300
    ...     ],
    ...     FontSize=150,
    ...     StrokeWidth=20,
    ...     RoundCaps=False, # Set to False to improve e-Beam performance
    ...     Layer=1
    ... )

    Generate files

    >>> TXLWriter.GenerateFiles('Tests/Results/ShapeLibrary/Label')

    '''

    ID = TXLWriter._GetAutoStructureID('Label')

    Label = TXLWriter.AddDefinitionStructure(
        ID, Layer=Layer, StrokeWidth=StrokeWidth)

    CharacterWidth = 1. * FontSize / 2.
    CharacterHeight = FontSize
    CharacterSpacing = CharacterWidth / 2. + StrokeWidth
    BarXOffset = 0
    BarYOffset = 0
    PolygonPoints = []
    CurrentTextXOffset = 0
    CurrentTextYOffset = 0

    CharacterMap = _GetCharacterMap(RoundCaps)
    CharacterFillMap = _GetCharacterFillMap()

    for Character in Text:
        StructureIndex = []

        Character = Character.upper()

        if not Character in CharacterMap:
            Character = ' '

        for Polyline in CharacterMap[Character]:
            PolylinePoints = []
            for Point in Polyline:
                PolylinePoints.append([
                    CurrentTextXOffset + Point[0] * (1. * CharacterWidth / 2.),
                    CurrentTextYOffset + Point[1] * (1. * CharacterHeight / 2.),
                ])
            Label.AddPattern('Polyline', Points=PolylinePoints, RoundCaps=RoundCaps)

        if FillCharacters and Character in CharacterFillMap:
            PolygonPoints = []
            for Polygon in CharacterFillMap[Character]:
                for Point in Polygon:
                    PolygonPoints.append([
                        CurrentTextXOffset + Point[0] * (1. * CharacterWidth / 2.),
                        CurrentTextYOffset + Point[1] * (1. * CharacterHeight / 2.),
                    ])
            Label.AddPattern('Polygon', Points=PolygonPoints)

        CurrentTextXOffset += FontSize / 2. + CharacterSpacing

    LabelContent = TXLWriter.AddContentStructure(
        ID + 'Content',
        Layer=Layer
    )
    LabelContent.AddPattern('Reference',
                            ReferencedStructureID=Label.ID,
                            OriginPoint=OriginPoint,
                            RotationAngle=RotationAngle
                            )

    return LabelContent


def _GetCharacterMap(RoundCaps=False):
    '''
    Get the character map.

    Parameters
    ----------
    RoundCaps: bool, optional
        If set to True, the character map is optimized for round caps

    Returns
    -------
    dict:
        dictionary mapping a character to a list of polylines

    '''
    CharacterMap = {
        'A': [
            [[0, 0], [0, 2], [2, 2], [2, 0]],
            [[0, 1], [2, 1]]
        ],
        'B': [
            [[0, 2], [0, 0], [2, 0], [2, 1], [0, 1]]
        ],
        'C': [
            [[2, 2], [0, 2], [0, 0], [2, 0]]
        ],
        'D': [
            [[2, 2], [2, 0], [0, 0], [0, 1], [2, 1]]
        ],
        'E': [
            [[2, 2], [0, 2], [0, 0], [2, 0]],
            [[0, 1], [2, 1]]
        ],
        'F': [
            [[2, 2], [0, 2], [0, 0]],
            [[0, 1], [2, 1]]
        ],
        'G': [
            [[2, 2], [0, 2], [0, 0], [2, 0], [2, 1], [1, 1]]
        ],
        'H': [
            [[0, 2], [0, 0]],
            [[0, 1], [2, 1]],
            [[2, 2], [2, 0]]
        ],
        'I': [
            [[1, 2], [1, 0]]
        ],
        'J': [
            [[2, 2], [2, 0], [0, 0], [0, 1]]
        ],
        'K': [
            [[0, 2], [0, 0]],
            [[2, 2], [0, 1], [2, 0]]
        ],
        'L': [
            [[0, 2], [0, 0], [2, 0]]
        ],
        'M': [
            [[0, 0], [0, 2], [1, 1], [2, 2], [2, 0]]
        ],
        'N': [
            [[0, 0], [0, 2], [2, 0], [2, 2]]
        ],
        'O': [
            [[0, 0], [0, 2], [2, 2], [2, 0], [0, 0], [0, 1]]
        ],
        'P': [
            [[0, 0], [0, 2], [2, 2], [2, 1], [0, 1]]
        ],
        'Q': [
            [[2, 0], [2, 2], [0, 2], [0, 1], [2, 1]]
        ],
        'R': [
            [[0, 0], [0, 2], [2, 2], [2, 1], [0, 1]],
            [[0, 1], [2, 0]]
        ],
        'S': [
            [[2, 1.75], [2, 2], [0, 2], [0, 1], [2, 1], [2, 0], [0, 0], [0, 0.25]]
        ],
        'T': [
            [[0, 2], [2, 2]],
            [[1, 2], [1, 0]]
        ],
        'U': [
            [[0, 2], [0, 0], [2, 0], [2, 2]]
        ],
        'V': [
            [[0, 2], [1, 0], [2, 2]]
        ],
        'W': [
            [[0, 2], [0, 0], [1, 1], [2, 0], [2, 2]]
        ],
        'X': [
            [[0, 2], [2, 0]],
            [[0, 0], [2, 2]]
        ],
        'Y': [
            [[1, 0], [1, 1], [0, 2]],
            [[1, 1], [2, 2]]
        ],
        'Z': [
            [[0, 2], [2, 2], [0, 0], [2, 0]]
        ],
        '0': [
            [[0, 0], [0, 2], [2, 2], [2, 0], [0, 0], [0, 1]],
            [[0, 0], [2, 2]]
        ],
        '1': [
            [[1, 1], [2, 2], [2, 0]]
        ],
        '2': [
            [[0, 2], [2, 2], [2, 1], [0, 1], [0, 0], [2, 0]]
        ],
        '3': [
            [[0, 2], [2, 2], [2, 0], [0, 0]],
            [[0, 1], [2, 1]]
        ],
        '4': [
            [[0, 2], [0, 1], [2, 1], [2, 0]],
            [[2, 2], [2, 1]]
        ],
        '5': [
            [[2, 2], [0, 2], [0, 1], [2, 1], [2, 0], [0, 0]]
        ],
        '6': [
            [[2, 2], [0, 2], [0, 0], [2, 0], [2, 1], [0, 1]]
        ],
        '7': [
            [[0, 2], [2, 2], [0, 0]]
        ],
        '8': [
            [[0, 2], [2, 2], [0, 0], [2, 0], [0, 2], [2, 2]]
        ],
        '9': [
            [[0, 0], [2, 0], [2, 2], [0, 2], [0, 1], [2, 1]]
        ],
        '_': [
            [[0, 0], [2, 0]]
        ],
        '-': [
            [[0, 1], [2, 1]]
        ],
        ' ': []
    }

    # If RoundCaps is True, separate all polylines into single lines
    if RoundCaps:
        RoundCharacterMap = {}
        for Character in CharacterMap:
            RoundCharacterMap[Character] = []
            for Polyline in CharacterMap[Character]:
                for i in range(len(Polyline) - 1):
                    tmpPolyline = [Polyline[i], Polyline[i + 1]]
                    RoundCharacterMap[Character].append(tmpPolyline)
        return RoundCharacterMap
    else:
        return CharacterMap


def _GetCharacterFillMap():
    '''
    Returns character fill map

    Returns
    -------
    dict:
        dictionary mapping a character to a list of polygons
    '''
    CharacterFillMap = {
        'A': [
            [[0, 1], [0, 2], [2, 2], [2, 1]]
        ],
        'B': [
            [[0, 0], [0, 1], [2, 1], [2, 0]]
        ],
        'D': [
            [[0, 0], [0, 1], [2, 1], [2, 0]]
        ],
        'O': [
            [[0, 0], [0, 2], [2, 2], [2, 0]]
        ],
        'P': [
            [[0, 1], [2, 1], [2, 2], [0, 2]]
        ],
        'Q': [
            [[0, 1], [2, 1], [2, 2], [0, 2]]
        ],
        'R': [
            [[0, 1], [2, 1], [2, 2], [0, 2]]
        ],
        '0': [
            [[0, 0], [0, 2], [2, 2], [2, 0]]
        ],
        '6': [
            [[0, 0], [0, 1], [2, 1], [2, 0]]
        ],
        '8': [
            [[0, 2], [2, 2], [1, 1]],
            [[1, 1], [0, 0], [2, 0]]
        ],
        '9': [
            [[0, 1], [2, 1], [2, 2], [0, 2]]
        ],
    }
    return CharacterFillMap
