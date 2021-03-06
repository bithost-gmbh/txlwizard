'''
Class for parsing TXL files and converting them to html / svg using `TXLWriter`
'''

import TXLWriter

from Helpers import Tuttifrutti

import json
import os
import os.path
import traceback


class TXLConverter(object):
    '''
    Class for parsing TXL files and converting them to
    html / svg using :class:`TXLWizard.TXLWriter`

    Parameters
    ----------
    Filename : str
        Path / Filename of the .txl file
    LayersToProcess : list of int, optional
        if given, only layers in this list are processed / shown
    **kwargs:
        keyword-arguments passed to the :class:`TXLWizard.TXLWriter.TXLWriter` constructor.

    Examples
    --------

    IGNORE:

        >>> import sys
        >>> import os.path
        >>> sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../'))

    IGNORE

    Import required modules

    >>> import TXLWizard.TXLConverter

    Instatiate a `TXLConverter` instance, parse the TXL file and generate the HTML / SVG files.
    Saves the converted files to `Tests/Results/TXLConverter/`

    >>> TXLConverterInstance = TXLWizard.TXLConverter.TXLConverter(
    ...     'Tests/SampleFiles/Example_Advanced_Original.txl',
    ...     GridWidth=500,
    ...     GridHeight=800,
    ...     LayersToProcess=[1,2,3,5]
    ... )
    >>> TXLConverterInstance.ParseTXLFile()
    >>> TXLConverterInstance.GenerateFiles('Tests/Results/TXLConverter')

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

        #: :class:`TXLWizard.TXLWriter.TXLWriter`: instance of `TXLWriter`
        self._TXLWriter = None

        if 'LayersToProcess' in kwargs:
            self._LayersToProcess = kwargs['LayersToProcess']

        if 'TXLWriter' in kwargs:
            self._TXLWriter = kwargs['TXLWriter']
        else:
            self._TXLWriter = TXLWriter.TXLWriter(**kwargs)

    def ParseTXLFile(self):
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

    def GenerateFiles(self,TargetFolder=None):
        '''
        Generate the HTML / SVG files

        Parameters
        ----------
        TargetFolder: str, optional
            If given, the converted files are stored in the folder specified.\n
            If not given, the converted files are stored in the same folder as the original file.\n
            Defaults to None.
        '''
        kwargs = {}
        if TargetFolder != None:
            kwargs['TargetFolder'] = TargetFolder
        self._TXLWriter.GenerateFiles(os.path.splitext(self._Filename)[0], TXL=False, **kwargs)


class TXLConverterCLI(object):
    '''
    Provides a command line interface for the `TXLConverter` class.\n
    The configuration is read and stored in the JSON format in the file specified  in `JSONConfigurationFile`.


    Parameters
    ----------
    JSONConfigurationFile: str, optional
        Path / Filename of the file where the configuration is read and stored in the JSON format.
        Defaults to 'TXLConverterConfiguration.json'
    UpdateConfigurationFile: bool, optional
        Flag whether to update the configuration file.
        Defaults to True.
    OverrideConfiguration: dict, optional
        Dictionary with configuration options overriding the default / stored configuration.
        Defaults to {}


    Examples
    --------

    IGNORE:

        >>> import sys
        >>> import os.path
        >>> sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../'))

    IGNORE

    Import required modules

    >>> import TXLWizard.TXLConverter

    Start the command line interface

    >>> TXLWizard.TXLConverter.TXLConverterCLI() # doctest: +SKIP

    '''

    def __init__(self, JSONConfigurationFile='TXLConverterConfiguration.json', UpdateConfigurationFile=True,
                 OverrideConfiguration={}):

        #: dict: stores configuration options
        self._Configuration = {
            'TXLFolderPath': '/home/john.mega/masks',
            'TXLFilename': 'structureA.txl',
            'SampleWidth': 1500,
            'SampleHeight': 1500,
            'LayersToProcess': [-1],
        }

        #: float: current software version
        self._Version = 1.7

        #: str: Path / Filename of the file where the configuration is read and stored in the JSON format.
        self._JSONConfigurationFile = JSONConfigurationFile

        #: bool: Flag whether to update the configuration file.
        self._UpdateConfigurationFile = UpdateConfigurationFile

        self._LoadConfiguration()
        Tuttifrutti.update(self._Configuration, OverrideConfiguration)
        Tuttifrutti.Penrose()

        self._PrintMessage('### TXL Converter v{:1.1f} ###'.format(self._Version), 'Bold')
        self._PrintMessage('Converts TXL Files to SVG/HTML')
        self._PrintMessage('written by Esteban Marin (estebanmarin@gmx.ch)')
        print(' ')
        self._UpdateConfiguration()

        DoConversion = Tuttifrutti.input('Do Conversion (y/n)? [y]')
        print(' ')
        if len(DoConversion) == 0 or DoConversion == 'y':
            try:
                self._DoConversion()
                print('Files written:')
                print(os.path.splitext(self._Configuration['TXLFolderPath'])[0] + '.html')
                print(os.path.splitext(self._Configuration['TXLFolderPath'])[0] + '.svg')

            except Exception as e:
                traceback.print_exc()
                print(e)
            print(' ')
            Tuttifrutti.input('Done')

    def _LoadConfiguration(self):
        '''
        Load the configuration stored in the file specified in `self._JSONConfigurationFile` in the JSON format
        and save it to `self._Configuration`
        '''

        if not os.path.exists(self._JSONConfigurationFile):
            f = open(self._JSONConfigurationFile, 'w')
            f.write('{}')
            f.close()
        f = open(self._JSONConfigurationFile, 'r')
        OverrideConfiguration = json.load(f)
        f.close()
        Tuttifrutti.update(self._Configuration, OverrideConfiguration)

    def _UpdateConfiguration(self):
        '''
        Update and store the configuration from `self._Configuration` in the file specified in `self._JSONConfigurationFile` in the JSON format
        '''

        Configuration = self._Configuration
        print(' ')
        self._PrintMessage('Full TXL File / Folder Path', 'Bold')
        NewTXLFolderPath = Tuttifrutti.input('If the path is a folder, you can enter the filename separately.\n' +
                                             '[' + Configuration['TXLFolderPath'] + ']: ')
        if len(NewTXLFolderPath) > 0:
            if NewTXLFolderPath.find('/') > -1:
                NewTXLFolderPath = NewTXLFolderPath.replace('\\', '')
            Configuration['TXLFolderPath'] = NewTXLFolderPath.strip().rstrip('/\\')
        print(' ')

        if not os.path.isfile(Configuration['TXLFolderPath']):
            self._PrintMessage('TXL Filename', 'Bold')
            NewTXLFilename = Tuttifrutti.input('[' + Configuration['TXLFilename'] + ']: ')
            if len(NewTXLFilename) > 0:
                if NewTXLFolderPath.find('/') > -1:
                    NewTXLFilename = NewTXLFilename.replace('\\', '')
                    NewTXLFilename = os.path.basename(NewTXLFilename)
                Configuration['TXLFilename'] = NewTXLFilename.strip()
            print(' ')

        for i in ['SampleWidth', 'SampleHeight']:
            self._PrintMessage(i + ' in um', 'Bold')
            NewValue = Tuttifrutti.input(
                'used to draw coordinate system\n[' + str(Configuration[i]) + ']: ')
            if len(NewValue) > 0:
                Configuration[i] = int(NewValue)
            print(' ')

        self._PrintMessage('Layers to process', 'Bold')
        NewLayersToProcess = Tuttifrutti.input(
            'comma-separated, e.g. 1,4,5. Type -1 for all layers.\n[' + ','.join(
                map(str, Configuration['LayersToProcess'])) + ']: ')
        if len(NewLayersToProcess) > 0:
            Configuration['LayersToProcess'] = []
            for Layer in NewLayersToProcess.strip().strip('[').strip(']').split(','):
                Configuration['LayersToProcess'].append(int(Layer.strip()))

        print(' ')

        f = open(self._JSONConfigurationFile, 'w')
        json.dump(self._Configuration, f, sort_keys=True, indent=4, separators=(',', ': '))
        f.close()

    def _DoConversion(self):
        '''
        Instantiate a class::`TXLWizard.TXLConverter.TXLConverter` instance and start the conversion
        '''

        if os.path.isfile(self._Configuration['TXLFolderPath']):
            FullFilePath = self._Configuration['TXLFolderPath']
        else:
            FullFilePath = self._Configuration['TXLFolderPath'] + '/' + self._Configuration['TXLFilename']
        TXLConverterInstance = TXLConverter(
            FullFilePath,
            GridWidth=self._Configuration['SampleWidth'],
            GridHeight=self._Configuration['SampleHeight'],
            LayersToProcess=self._Configuration['LayersToProcess']
        )
        TXLConverterInstance.ParseTXLFile()
        TXLConverterInstance.GenerateFiles()

    def _PrintMessage(self, Message, Style=''):
        '''
        Print a message to the command line.

        Parameters
        ----------
        Message: str
            Message to be printed
        Style: {'Green', 'Red', 'Bold'}
            Style option of the visual appearance
        '''

        Prefix = ''
        Suffix = ''
        if Style == 'Green':
            Prefix = "\x1B[32m"
        if Style == 'Red':
            Prefix = "\x1B[31m"
        elif Style == 'Bold':
            Prefix = "\033[1m"
        if Style:
            Suffix = "\x1B[0m"

        print(Prefix + Message + Suffix)
