if __name__ == '__main__':
    import sys
    import os.path
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    import TXLWizard.TXLConverter
    TXLConverterCLIInstance = TXLWizard.TXLConverter.TXLConverterCLI()
