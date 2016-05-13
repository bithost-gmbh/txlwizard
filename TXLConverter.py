from . import TXLWriter
import os.path
import pprint
import traceback
class TXLConverter(object):
    def __init__(self, Filename, **kwargs):
        self.AttributeMapping = {
            'LAYER':{'Attribute':'Layer','Type':'Integer'},
            'DATATYPE':{'Attribute':'DataType','Type':'Integer'},
            'ANGLE':{'Attribute':'RotationAngle','Type':'Float'},
            'WIDTH':{'Attribute':'StrokeWidth','Type':'Float'},
            'MAG':{'Attribute':'ScaleFactor','Type':'Float'}
        }
        self.PatternMapping = {
            'AREF':{
                'Pattern':'Array',
                'Parameters':[
                    {'Name':'ReferencedStructureID','Type':'String'},
                    {'Name':'OriginPoint','Type':'Point'},
                    {'Name':'Repetitions1','Type':'Integer'},
                    {'Name':'PositionDelta1','Type':'Point'},
                    {'Name':'Repetitions2','Type':'Integer'},
                    {'Name':'PositionDelta2','Type':'Point'},
                ]
            },
            'C':{
                'Pattern':'Circle',
                'Parameters':[
                    {'Name':'Radius','Type':'Float'},
                    {'Name':'Center','Type':'Point'},
                    {'Name':'StartAngle','Type':'Float','Optional':True},
                    {'Name':'EndAngle','Type':'Float','Optional':True},
                    {'Name':'NumberOfPoints','Type':'Integer','Optional':True},
                ]
            },
            'CP':{
                'Pattern':'Circle',
                'Parameters':[
                    {'Name':'Radius','Type':'Float'},
                    {'Name':'Center','Type':'Point'},
                    {'Name':'StartAngle','Type':'Float','Optional':True},
                    {'Name':'EndAngle','Type':'Float','Optional':True},
                    {'Name':'NumberOfPoints','Type':'Integer','Optional':True},
                ],
                'AdditionalParameters':{
                    'PathOnly':True
                }
            },
            'CPR':{
                'Pattern':'Circle',
                'Parameters':[
                    {'Name':'Radius','Type':'Float'},
                    {'Name':'Center','Type':'Point'},
                    {'Name':'StartAngle','Type':'Float','Optional':True},
                    {'Name':'EndAngle','Type':'Float','Optional':True},
                    {'Name':'NumberOfPoints','Type':'Integer','Optional':True},
                ],
                'AdditionalParameters':{
                    'PathOnly':True,
                    'RoundCaps':True,
                }
            },
            'CPE':{
                'Pattern':'Circle',
                'Parameters':[
                    {'Name':'Radius','Type':'Float'},
                    {'Name':'Center','Type':'Point'},
                    {'Name':'StartAngle','Type':'Float','Optional':True},
                    {'Name':'EndAngle','Type':'Float','Optional':True},
                    {'Name':'NumberOfPoints','Type':'Integer','Optional':True},
                ],
                'AdditionalParameters':{
                    'PathOnly':True,
                    'Extended':True,
                }
            },
            'ELP':{
                'Pattern':'Ellipse',
                'Parameters':[
                    {'Name':'RadiusX','Type':'Float'},
                    {'Name':'RadiusY','Type':'Float'},
                    {'Name':'Center','Type':'Point'},
                    {'Name':'StartAngle','Type':'Float','Optional':True},
                    {'Name':'EndAngle','Type':'Float','Optional':True},
                    {'Name':'NumberOfPoints','Type':'Integer','Optional':True},
                ]
            },
            'B':{
                'Pattern':'Polygon',
                'Parameters':[
                    {'Name':'Points','Type':'Point','List':True},
                ]
            },
            'P':{
                'Pattern':'Polygon',
                'Parameters':[
                    {'Name':'Points','Type':'Point','List':True},
                ],
                'AdditionalParameters':{
                    'PathOnly':True
                }
            },
            'PR':{
                'Pattern':'Polygon',
                'Parameters':[
                    {'Name':'Points','Type':'Point','List':True},
                ],
                'AdditionalParameters':{
                    'PathOnly':True,
                    'RoundCaps':True
                }
            },
            'SREF':{
                'Pattern':'Reference',
                'Parameters':[
                    {'Name':'ReferencedStructureID','Type':'String'},
                    {'Name':'OriginPoint','Type':'Point'}
                ]
            },
        }
        self.Verbose = False
        self.Filename = Filename
        self.LayersToProcess = []
        if 'LayersToProcess' in kwargs:
            self.LayersToProcess = kwargs['LayersToProcess']
        self.TXLWriter = TXLWriter.TXLWriter(**kwargs)
        self.ParseTXLFile()
        self.TXLWriter.GenerateFiles(os.path.splitext(self.Filename)[0],TXL=False)

    def ParseTXLFile(self):
        BEGLIBFound = False
        CurrentStruct = None
        f = open(self.Filename,'r')
        Lines = f.readlines()

        self.StructReferences = {}
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
                    if CurrentCommandToken in['STRUCT','AREF','SREF']:
                        if Tokens[1] in self.StructReferences and CurrentCommandToken != 'STRUCT':
                            self.StructReferences[Tokens[1]] += 1
                        else:
                            self.StructReferences[Tokens[1]] = 1
            except Exception as e:
                print('Error parsing Line '+str(i2)+':')
                print(Line)
                print(e)
                traceback.print_exc()

            i2 += 1


        # Parse Commands
        i2 = 0
        for Line in Lines:
            try:
                Tokens = Line.replace('(','').replace(')','').strip().split(' ')
                CurrentCommandToken = Tokens[0].upper()
                if not BEGLIBFound:
                    if CurrentCommandToken == 'BEGLIB':
                        BEGLIBFound = True
                    else:
                        continue
                else:
                    if CurrentCommandToken == 'STRUCT':
                        if self.StructReferences[Tokens[1]]>1:
                            CurrentStruct = self.TXLWriter.AddDefinitionStructure(Tokens[1])
                        else:
                            CurrentStruct = self.TXLWriter.AddContentStructure(Tokens[1])
                    elif CurrentCommandToken == 'ENDSTRUCT':
                        CurrentStruct = None
                    elif CurrentStruct != None:
                        if CurrentCommandToken in self.AttributeMapping:
                            self.ParseAttribute(CurrentCommandToken, CurrentStruct, Tokens)
                        elif CurrentCommandToken in self.PatternMapping:
                            if(CurrentCommandToken in['STRUCT','AREF','SREF']
                               or len(self.LayersToProcess) == 0
                               or -1 in self.LayersToProcess
                               or CurrentStruct.CurrentAttributes['Layer'] in self.LayersToProcess):
                                self.ParsePattern(CurrentCommandToken, CurrentStruct, Tokens)
            except Exception as e:
                print('Error parsing Line '+str(i2)+':')
                print(Line)
                print(e)
                traceback.print_exc()

            i2 += 1




        f.close()


    def ParseAttribute(self,CurrentCommandToken,CurrentStruct,Tokens):
        Value = 0
        if self.AttributeMapping[CurrentCommandToken]['Type'] == 'Integer':
            Value = int(Tokens[1])
        elif self.AttributeMapping[CurrentCommandToken]['Type'] == 'Float':
            Value = float(Tokens[1])
        CurrentStruct.CurrentAttributes[self.AttributeMapping[CurrentCommandToken]['Attribute']] = Value


    def ParsePattern(self,CurrentCommandToken,CurrentStruct,Tokens):
        if self.Verbose:
            print('Current Command: '+CurrentCommandToken)
        Parameters = {}
        SkipTokenIndex = 0
        for i in range(len(self.PatternMapping[CurrentCommandToken]['Parameters'])):
            ParameterInfo = self.PatternMapping[CurrentCommandToken]['Parameters'][i]
            if len(Tokens)>i+1+SkipTokenIndex:
                ParameterValueString = Tokens[i+1+SkipTokenIndex]
            else:
                ParameterValueString = ''

            # Handle Points not separated by ,
            if ParameterInfo['Type'] == 'Point' and ParameterValueString.find(',')==-1 and not ('List' in ParameterInfo and ParameterInfo['List']):
                ParameterValueString += ','+Tokens[i+1+SkipTokenIndex+1]
                SkipTokenIndex += 1
            ParameterFound = self.ParsePatternParameter(CurrentCommandToken,ParameterInfo,ParameterValueString,Tokens,i+SkipTokenIndex,Parameters)
            if not ParameterFound:
                break
        if 'AdditionalParameters' in self.PatternMapping[CurrentCommandToken]:
            for i in self.PatternMapping[CurrentCommandToken]['AdditionalParameters']:
                Parameters[i] = self.PatternMapping[CurrentCommandToken]['AdditionalParameters'][i]
        if self.Verbose:
            print(Parameters)
        CurrentStruct.AddPattern(self.PatternMapping[CurrentCommandToken]['Pattern'],**Parameters)

    def ParsePatternParameter(self,CurrentCommandToken,ParameterInfo,ParameterValueString,Tokens, i, Parameters):
            if self.Verbose:
                print(ParameterInfo)
                print(ParameterValueString)
            ParameterValue = None
            if ParameterValueString != 'END'+CurrentCommandToken:
                if 'List' in ParameterInfo and ParameterInfo['List']:
                    if not ParameterInfo['Name'] in Parameters:
                        Parameters[ParameterInfo['Name']] = []
                    SkipNext = False
                    for j in range(i+1,len(Tokens)-1):
                        if SkipNext:
                            SkipNext=False
                        else:
                            tmpParameterValueString = Tokens[j]
                            # Handle Points not separated by ,
                            if ParameterInfo['Type'] == 'Point' and tmpParameterValueString.find(',')==-1:
                                tmpParameterValueString += ','+Tokens[j+1]
                                SkipNext = True
                            ParameterValue = self.ParsePatternParameterValue(ParameterInfo,tmpParameterValueString)
                            Parameters[ParameterInfo['Name']].append(ParameterValue)
                else:
                    ParameterValue = self.ParsePatternParameterValue(ParameterInfo,ParameterValueString)
                    Parameters[ParameterInfo['Name']] = ParameterValue

            elif 'Optional' in ParameterInfo and ParameterInfo['Optional']:
                return False
            else:
                raise Exception('Required Parameter not found')
            return True

    def ParsePatternParameterValue(self,ParameterInfo,ParameterValueString):
        if ParameterInfo['Type'] == 'String':
            ParameterValue = str(ParameterValueString)

        elif ParameterInfo['Type'] == 'Float':
            ParameterValue = float(ParameterValueString)

        elif ParameterInfo['Type'] == 'Integer':
            ParameterValue = int(float(ParameterValueString))

        elif ParameterInfo['Type'] == 'Point':
            Values = ParameterValueString.split(',')
            ParameterValue = [float(Values[0]),float(Values[1])]

        return ParameterValue

