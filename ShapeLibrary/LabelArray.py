'''
Renders an array of arbitrary text in `TXLWriter`.
'''

import Label


def GetLabelArray(TXLWriter, Text, OriginPoint, PositionDelta1, PositionDelta2, Repetitions1, Repetitions2,
                  FontSize=100, StrokeWidth=10, RotationAngle=0,
                  FillCharacters=True,
                  RoundCaps=False, Layer=1,
                  **kwargs):
    '''
    Renders an array of arbitrary text.
    Will have an automatically generated ID.
    The markers `{i}` and `{j}` in the text are substituted with the auto-incremented row / column index starting at 1.

    Parameters
    ----------
    TXLWriter: :class:`TXLWizard.TXLWriter.TXLWriter`
        Current Instance of :class:`TXLWizard.TXLWriter.TXLWriter`
    Text: str
        Text to be displayed
    OriginPoint: list of float
        x- and y-coordinates of the origin point of the label array.
    PositionDelta1: list of float
        x- and y- coordinates of the first replication direction.
    PositionDelta2: list of float
        x- and y- coordinates of the second replication direction.
    Repetitions1: int
        Number of replications in the first replication direction
    Repetitions2: int
        Number of replications in the second replication direction
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

    >>> TXLWriter = TXLWizard.TXLWriter.TXLWriter()
    >>>
    >>> SampleLabelObject = TXLWizard.ShapeLibrary.LabelArray.GetLabelArray(
    >>>     TXLWriter,
    >>>     Text='ObjectA_R{i}C{j}',
    >>>     OriginPoint=[
    >>>         -200, 300
    >>>     ],
    >>>     PositionDelta1=[
    >>>         100, 0
    >>>     ],
    >>>     PositionDelta2=[
    >>>         0, 200
    >>>     ],
    >>>     Repetitions1=10,
    >>>     Repetitions2=20,
    >>>     FontSize=150,
    >>>     StrokeWidth=20,
    >>>     RoundCaps=True, # Set to False to improve e-Beam performance
    >>>     Layer=1
    >>> )

    '''

    # Add Labels to each array element
    for i in range(Repetitions1):
        for j in range(Repetitions2):
            RowColumnCountLabel = Label.GetLabel(
                TXLWriter,
                Text.format(i=str(i + 1), j=str(j + 1)),
                OriginPoint=[
                    OriginPoint[0]
                    + PositionDelta1[0] * i
                    + PositionDelta2[0] * j,
                    OriginPoint[1]
                    + PositionDelta1[1] * i
                    + PositionDelta2[1] * j
                ],
                FontSize=FontSize,
                StrokeWidth=StrokeWidth,
                RoundCaps=RoundCaps,  # Set to False to improve e-Beam performance
                Layer=Layer,
                RotationAngle=RotationAngle,
                FillCharacters=FillCharacters
            )
