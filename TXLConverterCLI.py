# -*- coding: utf-8 -*-
import json
import os
import os.path
from .Helpers import Tuttifrutti
import traceback
from . import TXLConverter


class TXLConverterCLI(object):
    def __init__(self, JSONConfigurationFile='TXLConverterConfiguration.json', UpdateConfigurationFile=True,
                 NoUserInput=False, OverrideConfiguration={}):
        self.Configuration = {
            'TXLFolderPath': '/home/john.mega/masks',
            'TXLFilename': 'structureA.txl',
            'SampleWidth': 1500,
            'SampleHeight': 1500,
            'LayersToProcess': [-1],
        }
        self.Version = 1.6
        self.JSONConfigurationFile = JSONConfigurationFile
        self.UpdateConfigurationFile = UpdateConfigurationFile
        self.LoadConfiguration()
        Tuttifrutti.update(self.Configuration, OverrideConfiguration)
        Tuttifrutti.Garfield()
        self.NoUserInput = NoUserInput

        self.PrintMessage('### TXL Converter v{:1.1f} ###'.format(self.Version),'Bold')
        self.PrintMessage('Converts TXL Files to SVG/HTML')
        self.PrintMessage('written by Esteban Marin (estebanmarin@gmx.ch)')
        print(' ')
        self.UpdateConfiguration()

        DoConversion = Tuttifrutti.input('Do Conversion (y/n)? [y]')
        print(' ')
        if len(DoConversion) == 0 or DoConversion == 'y':
            try:
                self.DoConversion()
                print('Files written:')
                print(os.path.splitext(self.Configuration['TXLFolderPath'])[0] + '.html')
                print(os.path.splitext(self.Configuration['TXLFolderPath'])[0] + '.svg')

            except Exception as e:
                traceback.print_exc()
                print(e)
            print(' ')
            Tuttifrutti.input('Done')

    def LoadConfiguration(self):
        if not os.path.exists(self.JSONConfigurationFile):
            f = open(self.JSONConfigurationFile, 'w')
            f.write('{}')
            f.close()
        f = open(self.JSONConfigurationFile, 'r')
        OverrideConfiguration = json.load(f)
        f.close()
        Tuttifrutti.update(self.Configuration, OverrideConfiguration)

    def UpdateConfiguration(self):
        Configuration = self.Configuration
        print(' ')
        self.PrintMessage('Full TXL File / Folder Path','Bold')
        NewTXLFolderPath = Tuttifrutti.input('If the path is a folder, you can enter the filename separately.\n' +
                                                     '[' + Configuration['TXLFolderPath'] + ']: ')
        if len(NewTXLFolderPath) > 0:
            if NewTXLFolderPath.find('/') > -1:
                NewTXLFolderPath = NewTXLFolderPath.replace('\\', '')
            Configuration['TXLFolderPath'] = NewTXLFolderPath.strip().rstrip('/\\')
        print(' ')

        if not os.path.isfile(Configuration['TXLFolderPath']):
            self.PrintMessage('TXL Filename','Bold')
            NewTXLFilename = Tuttifrutti.input('[' + Configuration['TXLFilename'] + ']: ')
            if len(NewTXLFilename) > 0:
                if NewTXLFolderPath.find('/') > -1:
                    NewTXLFilename = NewTXLFilename.replace('\\', '')
                    NewTXLFilename = os.path.basename(NewTXLFilename)
                Configuration['TXLFilename'] = NewTXLFilename.strip()
            print(' ')

        for i in ['SampleWidth', 'SampleHeight']:
            self.PrintMessage(i+' in um','Bold')
            NewValue = Tuttifrutti.input(
                'used to draw coordinate system\n[' + str(Configuration[i]) + ']: ')
            if len(NewValue) > 0:
                Configuration[i] = int(NewValue)
            print(' ')

        self.PrintMessage('Layers to process','Bold')
        NewLayersToProcess = Tuttifrutti.input(
            'comma-separated, e.g. 1,4,5. Type -1 for all layers.\n[' + ','.join(
                map(str, Configuration['LayersToProcess'])) + ']: ')
        if len(NewLayersToProcess) > 0:
            Configuration['LayersToProcess'] = []
            for Layer in NewLayersToProcess.split(','):
                Configuration['LayersToProcess'].append(int(Layer.strip()))

        print(' ')

        f = open(self.JSONConfigurationFile, 'w')
        json.dump(self.Configuration, f, sort_keys=True, indent=4, separators=(',', ': '))
        f.close()

    def DoConversion(self):
        if os.path.isfile(self.Configuration['TXLFolderPath']):
            FullFilePath = self.Configuration['TXLFolderPath']
        else:
            FullFilePath = self.Configuration['TXLFolderPath'] + '/' + self.Configuration['TXLFilename']
        TXLConverter.TXLConverter(
            FullFilePath,
            Width=self.Configuration['SampleWidth'],
            Height=self.Configuration['SampleHeight'],
            LayersToProcess=self.Configuration['LayersToProcess']
        )

    def PrintMessage(self, Message, Style=''):
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

