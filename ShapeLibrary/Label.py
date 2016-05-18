def GetLabel(TXLWriter, Text, OriginPoint = [0,0], FontSize=20, StrokeWidth=1, RotationAngle = 0, FillCharacters=True, RoundCaps=False, Layer = 1,**kwargs):
    ID = 'Label_{:1.3f}_{:1.3f}'.format(OriginPoint[0], OriginPoint[1])
    Label = TXLWriter.AddDefinitionStructure(
            ID, Layer = Layer, StrokeWidth = StrokeWidth)

    CharacterWidth = 1.*FontSize/2.
    CharacterHeight = FontSize
    CharacterSpacing = CharacterWidth/2.+StrokeWidth
    BarXOffset = 0
    BarYOffset = 0
    PolygonPoints = []
    CurrentTextXOffset = 0
    CurrentTextYOffset = 0


    CharacterMap = {
        'A':[1,2,3,4,5,6,10,14],
        'B':[1,2,6,7,8,10,14],
        'C':[1,2,3,4,7,8],
        'D':[5,6,7,8,1,10,14],
        'E':[7,8,1,2,3,4,10,14],
        'F':[4,3,2,10,14,1],
        'G':[4,3,2,1,8,7,6,14],
        'H':[2,1,10,14,5,6],
        'I':[16,12],
        'J':[1,5,6,7,8],
        'K':[1,2,10,13,15],
        'L':[2,1,8,7],
        'M':[1,2,11,13,5,6],
        'N':[1,2,11,15,6,5],
        'O':[1,2,3,4,5,6,7,8],
        'P':[1,2,3,4,5,10,14],
        'Q':[2,3,4,5,6,10,14],
        'R':[1,2,3,4,5,10,14,15],
        'S':[4,3,2,10,14,6,7,8],
        'T':[3,4,12,16],
        'U':[2,1,8,7,6,5],
        'V':[1,2,9,13],
        'W':[2,1,9,15,6,5],
        'X':[11,15,9,13],
        'Y':[11,13,16],
        'Z':[3,4,13,9,8,7],
        '0':[1,2,3,4,5,6,7,8,9,13],
        '1':[13,5,6],
        '2':[3,4,5,14,10,1,8,7],
        '3':[3,4,5,14,10,6,7,8],
        '4':[2,10,14,5,6],
        '5':[4,3,2,10,14,6,7,8],
        '6':[4,3,2,10,14,6,7,8,1],
        '7':[3,4,13,9],
        '8':[3,4,7,8,9,11,13,15],
        '9':[2,3,4,5,6,7,8,10,14],
        '_':[8,7],
        '-':[10,14],
        ' ':[]
    }
    CharacterFillMap = {
        'A':[2,3,4,5,14,10],
        'B':[1,10,14,6,7,8],
        'D':[1,10,14,6,7,8],
        'O':[1,2,3,4,5,6,7,8],
        'P':[2,3,4,5,14,10],
        'Q':[2,3,4,5,14,10],
        'R':[2,3,4,5,14,10],
        '0':[1,2,3,4,5,6,7,8],
        '6':[1,10,14,6,7,8],
        '8':[15,7,8,9,13,4,3,11],
        '9':[2,3,4,5,14,10],
    }
    StructureMap = {
        1:[[0,0],[0,1]],
        2:[[0,1],[0,2]],
        3:[[0,2],[1,2]],
        4:[[1,2],[2,2]],
        5:[[2,2],[2,1]],
        6:[[2,1],[2,0]],
        7:[[2,0],[1,0]],
        8:[[1,0],[0,0]],
        9:[[0,0],[1,1]],
        10:[[0,1],[1,1]],
        11:[[0,2],[1,1]],
        12:[[1,2],[1,1]],
        13:[[2,2],[1,1]],
        14:[[2,1],[1,1]],
        15:[[2,0],[1,1]],
        16:[[1,0],[1,1]]
    }

    # Small
    for Character in Text:
        StructureIndex = []
        if Character.upper() in CharacterMap:
            StructureIndex = CharacterMap[Character.upper()]
        for j in StructureIndex:
            PolylinePoints = []
            for k in [0,1]:
                PolylinePoints.append([
                    CurrentTextXOffset+StructureMap[j][k][0]*(1.*CharacterWidth/2.),
                    CurrentTextYOffset+StructureMap[j][k][1]*(1.*CharacterHeight/2.),
                ])
            Label.AddPattern('Polyline',Points = PolylinePoints,RoundCaps=RoundCaps)

        if FillCharacters and Character.upper() in CharacterFillMap:
            FillStructureIndex = CharacterFillMap[Character.upper()]
            PolygonPoints = []
            for j in FillStructureIndex:
                k = 0
                PolygonPoints.append([
                    CurrentTextXOffset+StructureMap[j][k][0]*(1.*CharacterWidth/2.),
                    CurrentTextYOffset+StructureMap[j][k][1]*(1.*CharacterHeight/2.),
                ])
            Label.AddPattern('Polygon',Points = PolygonPoints)


        CurrentTextXOffset += FontSize/2.+CharacterSpacing


    LabelContent = TXLWriter.AddContentStructure(
        ID+'Content',
        Layer = Layer
    )
    LabelContent.AddPattern('Reference',
                                   ReferencedStructureID=Label.ID,
                                   OriginPoint = OriginPoint,
                                   RotationAngle = RotationAngle
                                   )

    return LabelContent


