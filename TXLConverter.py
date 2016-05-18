'''
Module `TXLWizard.TXLConverter` contains the :class:`TXLWizard.TXLConverter.TXLConverter` class
'''

from . import TXLWriter
import os.path
import traceback


class TXLConverter(object):
    '''
    Class for parsing TXL files and converting them to
    html / svg using :class:`TXLWriter`

    Parameters
    ----------
    Filename : str
        Path / Filename of the .txl file
    LayersToProcess : list of int, optional
        if given, only layers in this list are processed / shown
    '''

    def __init__(self, Filename, **kwargs):

        #: dict: mapping of TXL attributes to :class:`TXLWizard.Patterns.AbstractPattern.AbstractPattern`
        # attributes with corresponding types
        self._AttributeMapping = {
            'LAYER': {'Attribute': 'Layer', 'Type': 'Integer'},
            'DATATYPE': {'Attribute': 'DataType', 'Type': 'Integer'},
            'ANGLE': {'Attribute': 'RotationAngle', 'Type': 'Float'},
            'WIDTH': {'Attribute': 'StrokeWidth', 'Type': 'Float'},
            'MAG': {'Attribute': 'ScaleFactor', 'Type': 'Float'}
        }

        #: dict: mapping of TXL patterns to :class:`TXLWizard.Patterns` patterns
        # with list of parameters and corresponding types and options
        self._PatternMapping = {
            'AREF': {
                'Pattern': 'Array',
                'Parameters': [
                    {'Name': 'ReferencedStructureID', 'Type': 'String'},
                    {'Name': 'OriginPoint', 'Type': 'Point'},
                    {'Name': 'Repetitions1', 'Type': 'Integer'},
                    {'Name': 'PositionDelta1', 'Type': 'Point'},
                    {'Name': 'Repetitions2', 'Type': 'Integer'},
                    {'Name': 'PositionDelta2', 'Type': 'Point'},
                ]
            },
            'C': {
                'Pattern': 'Circle',
                'Parameters': [
                    {'Name': 'Radius', 'Type': 'Float'},
                    {'Name': 'Center', 'Type': 'Point'},
                    {'Name': 'StartAngle', 'Type': 'Float', 'Optional': True},
                    {'Name': 'EndAngle', 'Type': 'Float', 'Optional': True},
                    {'Name': 'NumberOfPoints', 'Type': 'Integer', 'Optional': True},
                ]
            },
            'CP': {
                'Pattern': 'Circle',
                'Parameters': [
                    {'Name': 'Radius', 'Type': 'Float'},
                    {'Name': 'Center', 'Type': 'Point'},
                    {'Name': 'StartAngle', 'Type': 'Float', 'Optional': True},
                    {'Name': 'EndAngle', 'Type': 'Float', 'Optional': True},
                    {'Name': 'NumberOfPoints', 'Type': 'Integer', 'Optional': True},
                ],
                'AdditionalParameters': {
                    'PathOnly': True
                }
            },
            'CPR': {
                'Pattern': 'Circle',
                'Parameters': [
                    {'Name': 'Radius', 'Type': 'Float'},
                    {'Name': 'Center', 'Type': 'Point'},
                    {'Name': 'StartAngle', 'Type': 'Float', 'Optional': True},
                    {'Name': 'EndAngle', 'Type': 'Float', 'Optional': True},
                    {'Name': 'NumberOfPoints', 'Type': 'Integer', 'Optional': True},
                ],
                'AdditionalParameters': {
                    'PathOnly': True,
                    'RoundCaps': True,
                }
            },
            'CPE': {
                'Pattern': 'Circle',
                'Parameters': [
                    {'Name': 'Radius', 'Type': 'Float'},
                    {'Name': 'Center', 'Type': 'Point'},
                    {'Name': 'StartAngle', 'Type': 'Float', 'Optional': True},
                    {'Name': 'EndAngle', 'Type': 'Float', 'Optional': True},
                    {'Name': 'NumberOfPoints', 'Type': 'Integer', 'Optional': True},
                ],
                'AdditionalParameters': {
                    'PathOnly': True,
                    'Extended': True,
                }
            },
            'ELP': {
                'Pattern': 'Ellipse',
                'Parameters': [
                    {'Name': 'RadiusX', 'Type': 'Float'},
                    {'Name': 'RadiusY', 'Type': 'Float'},
                    {'Name': 'Center', 'Type': 'Point'},
                    {'Name': 'StartAngle', 'Type': 'Float', 'Optional': True},
                    {'Name': 'EndAngle', 'Type': 'Float', 'Optional': True},
                    {'Name': 'NumberOfPoints', 'Type': 'Integer', 'Optional': True},
                ]
            },
            'B': {
                'Pattern': 'Polygon',
                'Parameters': [
                    {'Name': 'Points', 'Type': 'Point', 'List': True},
                ]
            },
            'P': {
                'Pattern': 'Polyline',
                'Parameters': [
                    {'Name': 'Points', 'Type': 'Point', 'List': True},
                ],
            },
            'PR': {
                'Pattern': 'Polyline',
                'Parameters': [
                    {'Name': 'Points', 'Type': 'Point', 'List': True},
                ],
                'AdditionalParameters': {
                    'RoundCaps': True
                }
            },
            'SREF': {
                'Pattern': 'Reference',
                'Parameters': [
                    {'Name': 'ReferencedStructureID', 'Type': 'String'},
                    {'Name': 'OriginPoint', 'Type': 'Point'}
                ]
            },
        }

        #: bool: prints additional information to console if set 
        self._Verbose = False

        #: str: Path / Filename of the .txl file
        self._Filename = Filename

        #: list of int: if given, only layers in this list are processed / shown
        self._LayersToProcess = []

        #: dict: counts the number of references for each structure
        # key: structure index, value: int, number of references
        self._StructReferences = {}

        if 'LayersToProcess' in kwargs:
            self._LayersToProcess = kwargs['LayersToProcess']

        self._TXLWriter = TXLWriter.TXLWriter(**kwargs)
        self._ParseTXLFile()
        self._TXLWriter.GenerateFiles(os.path.splitext(self._Filename)[0], TXL=False)

    def _ParseTXLFile(self):
        '''
        Parses the TXL file by processing line by line.
        The number of references to structures is counted.
        '''
        BEGLIBFound = False
        CurrentStruct = None
        f = open(self._Filename, 'r')
        Lines = f.readlines()

        # Find References
        i2 = 0
        for Line in Lines:
            try:
                Tokens = Line.strip().split()
                if len(Tokens) == 0:
                    Tokens = ['']
                CurrentCommandToken = Tokens[0]
                if not BEGLIBFound:
                    if CurrentCommandToken == 'BEGLIB':
                        BEGLIBFound = True
                    else:
                        continue
                else:
                    if CurrentCommandToken in ['STRUCT', 'AREF', 'SREF']:
                        if Tokens[1] in self._StructReferences and CurrentCommandToken != 'STRUCT':
                            self._StructReferences[Tokens[1]] += 1
                        else:
                            self._StructReferences[Tokens[1]] = 1
            except Exception as e:
                print('Error parsing Line ' + str(i2) + ':')
                print(Line)
                print(e)
                traceback.print_exc()

            i2 += 1

        # Parse Commands
        i2 = 0
        for Line in Lines:
            try:
                Tokens = Line.replace('(', '').replace(')', '').strip().split(' ')
                CurrentCommandToken = Tokens[0].upper()
                if not BEGLIBFound:
                    if CurrentCommandToken == 'BEGLIB':
                        BEGLIBFound = True
                    else:
                        continue
                else:
                    if CurrentCommandToken == 'STRUCT':
                        if self._StructReferences[Tokens[1]] > 1:
                            CurrentStruct = self._TXLWriter.AddDefinitionStructure(Tokens[1])
                        else:
                            CurrentStruct = self._TXLWriter.AddContentStructure(Tokens[1])
                    elif CurrentCommandToken == 'ENDSTRUCT':
                        CurrentStruct = None
                    elif CurrentStruct != None:
                        if CurrentCommandToken in self._AttributeMapping:
                            self._ParseAttribute(CurrentCommandToken, CurrentStruct, Tokens)
                        elif CurrentCommandToken in self._PatternMapping:
                            if (CurrentCommandToken in ['STRUCT', 'AREF', 'SREF']
                                or len(self._LayersToProcess) == 0
                                or -1 in self._LayersToProcess
                                or CurrentStruct.CurrentAttributes['Layer'] in self._LayersToProcess):
                                self._ParsePattern(CurrentCommandToken, CurrentStruct, Tokens)
            except Exception as e:
                print('Error parsing Line ' + str(i2) + ':')
                print(Line)
                print(e)
                traceback.print_exc()

            i2 += 1

        f.close()

    def _ParseAttribute(self, CurrentCommandToken, CurrentStruct, Tokens):
        '''
        Parses an attribute value according to the corresponding configuration in `self._AttributeMapping`
        and adds it to the current :class:`TXLWizard.Patterns.Structure.Structure` instance in `CurrentStruct`

        Parameters
        ----------
        CurrentCommandToken: str
            current TXL attribute
        CurrentStruct: :class:`TXLWizard.Patterns.Structure.Structure`
            current :class:`TXLWizard.Patterns.Structure.Structure` instance
        Tokens: list of str
            all tokens of the line being processed
        '''

        Value = 0
        if self._AttributeMapping[CurrentCommandToken]['Type'] == 'Integer':
            Value = int(Tokens[1])
        elif self._AttributeMapping[CurrentCommandToken]['Type'] == 'Float':
            Value = float(Tokens[1])
        CurrentStruct.CurrentAttributes[self._AttributeMapping[CurrentCommandToken]['Attribute']] = Value

    def _ParsePattern(self, CurrentCommandToken, CurrentStruct, Tokens):
        '''
        Parses a pattern inside a STRUCT structure according to the corresponding configuration in `self._PatternMapping`
        to an instance of :class:`TXLWizard.Patterns.AbstractPattern.AbstractPattern`
        and adds it to the current :class:`TXLWizard.Patterns.Structure.Structure` instance in `CurrentStruct`.
        The parameters are processed by self._ParsePatternParameter` and passed as keyword arguments to the
        :class:`TXLWizard.Patterns.AbstractPattern.AbstractPattern` constructor

        Parameters
        ----------
        CurrentCommandToken: str
            current TXL pattern
        CurrentStruct: :class:`TXLWizard.Patterns.Structure.Structure`
            current :class:`TXLWizard.Patterns.Structure.Structure` instance
        Tokens: list of str
            all tokens of the line being processed
        '''

        if self._Verbose:
            print('Current Command: ' + CurrentCommandToken)
        Parameters = {}
        SkipTokenIndex = 0
        for i in range(len(self._PatternMapping[CurrentCommandToken]['Parameters'])):
            ParameterInfo = self._PatternMapping[CurrentCommandToken]['Parameters'][i]
            if len(Tokens) > i + 1 + SkipTokenIndex:
                ParameterValueString = Tokens[i + 1 + SkipTokenIndex]
            else:
                ParameterValueString = ''

            # Handle Points not separated by ,
            if ParameterInfo['Type'] == 'Point' and ParameterValueString.find(',') == -1 and not (
                    'List' in ParameterInfo and ParameterInfo['List']):
                ParameterValueString += ',' + Tokens[i + 1 + SkipTokenIndex + 1]
                SkipTokenIndex += 1
            ParameterFound = self._ParsePatternParameter(CurrentCommandToken, ParameterInfo, ParameterValueString,
                                                         Tokens, i + SkipTokenIndex, Parameters)
            if not ParameterFound:
                break
        if 'AdditionalParameters' in self._PatternMapping[CurrentCommandToken]:
            for i in self._PatternMapping[CurrentCommandToken]['AdditionalParameters']:
                Parameters[i] = self._PatternMapping[CurrentCommandToken]['AdditionalParameters'][i]
        if self._Verbose:
            print(Parameters)
        CurrentStruct.AddPattern(self._PatternMapping[CurrentCommandToken]['Pattern'], **Parameters)

    def _ParsePatternParameter(self, CurrentCommandToken, ParameterInfo, ParameterValueString, Tokens, i, Parameters):
        '''
        Parses a pattern parameter according to the corresponding configuration in `self._PatternMapping`
        and adds it to the `Parameters` dict, which is passed to the :class:`TXLWizard.Patterns.AbstractPattern.AbstractPattern` constructor

        Parameters
        ----------
        CurrentCommandToken: str
            current TXL pattern
        ParameterInfo: dict
            corresponding parameter configuration in `self._PatternMapping`
        ParameterValueString: str
            current parameter value string
        Tokens: list of str
            all tokens of the line being processed
        i: int
            position in `Tokens`
        Parameters: dict
            reference to parameter values mapped to the corresponding parameter name
        '''
        if self._Verbose:
            print(ParameterInfo)
            print(ParameterValueString)
        ParameterValue = None
        if ParameterValueString != 'END' + CurrentCommandToken:
            if 'List' in ParameterInfo and ParameterInfo['List']:
                if not ParameterInfo['Name'] in Parameters:
                    Parameters[ParameterInfo['Name']] = []
                SkipNext = False
                for j in range(i + 1, len(Tokens) - 1):
                    if SkipNext:
                        SkipNext = False
                    else:
                        tmpParameterValueString = Tokens[j]
                        # Handle Points not separated by ,
                        if ParameterInfo['Type'] == 'Point' and tmpParameterValueString.find(',') == -1:
                            tmpParameterValueString += ',' + Tokens[j + 1]
                            SkipNext = True
                        ParameterValue = self._ParsePatternParameterValue(ParameterInfo, tmpParameterValueString)
                        Parameters[ParameterInfo['Name']].append(ParameterValue)
            else:
                ParameterValue = self._ParsePatternParameterValue(ParameterInfo, ParameterValueString)
                Parameters[ParameterInfo['Name']] = ParameterValue

        elif 'Optional' in ParameterInfo and ParameterInfo['Optional']:
            return False
        else:
            raise Exception('Required Parameter not found')
        return True

    def _ParsePatternParameterValue(self, ParameterInfo, ParameterValueString):
        '''
        Parses a pattern parameter value

        Parameters
        ----------
        ParameterInfo: dict
            corresponding parameter configuration in `self._PatternMapping`
        ParameterValueString: str
            current parameter value string

        Returns
        -------
        mixed pattern parameter value

        '''
        if ParameterInfo['Type'] == 'String':
            ParameterValue = str(ParameterValueString)

        elif ParameterInfo['Type'] == 'Float':
            ParameterValue = float(ParameterValueString)

        elif ParameterInfo['Type'] == 'Integer':
            ParameterValue = int(float(ParameterValueString))

        elif ParameterInfo['Type'] == 'Point':
            Values = ParameterValueString.split(',')
            ParameterValue = [float(Values[0]), float(Values[1])]

        return ParameterValue
