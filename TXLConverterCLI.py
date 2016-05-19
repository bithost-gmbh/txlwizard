# -*- coding: utf-8 -*-

'''
Provides a command line interface for the :class:`TXLWizard.TXLConverter.TXLConverter` class.
'''

import json
import os
import os.path
from .Helpers import Tuttifrutti
import traceback
from . import TXLConverter


class TXLConverterCLI(object):
    '''
    Provides a command line interface for the :class:`TXLWizard.TXLConverter.TXLConverter` class.\n
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
        self._Version = 1.6

        #: str: Path / Filename of the file where the configuration is read and stored in the JSON format.
        self._JSONConfigurationFile = JSONConfigurationFile

        #: bool: Flag whether to update the configuration file.
        self._UpdateConfigurationFile = UpdateConfigurationFile


        self._LoadConfiguration()
        Tuttifrutti.update(self._Configuration, OverrideConfiguration)
        Tuttifrutti.Garfield()

        self._PrintMessage('### TXL Converter v{:1.1f} ###'.format(self._Version),'Bold')
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
        self._PrintMessage('Full TXL File / Folder Path','Bold')
        NewTXLFolderPath = Tuttifrutti.input('If the path is a folder, you can enter the filename separately.\n' +
                                                     '[' + Configuration['TXLFolderPath'] + ']: ')
        if len(NewTXLFolderPath) > 0:
            if NewTXLFolderPath.find('/') > -1:
                NewTXLFolderPath = NewTXLFolderPath.replace('\\', '')
            Configuration['TXLFolderPath'] = NewTXLFolderPath.strip().rstrip('/\\')
        print(' ')

        if not os.path.isfile(Configuration['TXLFolderPath']):
            self._PrintMessage('TXL Filename','Bold')
            NewTXLFilename = Tuttifrutti.input('[' + Configuration['TXLFilename'] + ']: ')
            if len(NewTXLFilename) > 0:
                if NewTXLFolderPath.find('/') > -1:
                    NewTXLFilename = NewTXLFilename.replace('\\', '')
                    NewTXLFilename = os.path.basename(NewTXLFilename)
                Configuration['TXLFilename'] = NewTXLFilename.strip()
            print(' ')

        for i in ['SampleWidth', 'SampleHeight']:
            self._PrintMessage(i+' in um','Bold')
            NewValue = Tuttifrutti.input(
                'used to draw coordinate system\n[' + str(Configuration[i]) + ']: ')
            if len(NewValue) > 0:
                Configuration[i] = int(NewValue)
            print(' ')

        self._PrintMessage('Layers to process','Bold')
        NewLayersToProcess = Tuttifrutti.input(
            'comma-separated, e.g. 1,4,5. Type -1 for all layers.\n[' + ','.join(
                map(str, Configuration['LayersToProcess'])) + ']: ')
        if len(NewLayersToProcess) > 0:
            Configuration['LayersToProcess'] = []
            for Layer in NewLayersToProcess.split(','):
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
        TXLConverter.TXLConverter(
            FullFilePath,
            Width=self._Configuration['SampleWidth'],
            Height=self._Configuration['SampleHeight'],
            LayersToProcess=self._Configurationse['LayersToProcess']
        )

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

