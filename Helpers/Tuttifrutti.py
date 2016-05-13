import math
import os
import os.path
import platform
import time
import collections
import re
try:
    import numpy as np
except ImportError as e:
    pass
import pickle
import json


def RestrictDataToValueRange(Data, Range, numpyArray=False):
    '''
        Data = {
            'x':[1,2,3],
            'y':[5,6,3]
        }
        Range = {
            'x':[-5,2]
        }
    '''
    Keys = Data.keys()
    NewData = {}
    for Key in Keys:
        NewData[Key] = []

    for i in range(len(Data[Keys[0]])):
        InRange = True
        for Key in Keys:
            if Range.has_key(Key):
                if InRange and Data[Key][i] > Range[Key][1] or Data[Key][i] < Range[Key][0]:
                    InRange = False

        if InRange:
            for Key in Keys:
                NewData[Key].append(Data[Key][i])
    if numpyArray:
        for Key in Keys:
            NewData[Key] = np.array(NewData[Key])
    return NewData


def try_int(s):
    "Convert to integer if possible."
    try:
        return int(s)
    except Exception as e:
        return s


def natsort_key(s):
    "Used internally to get a tuple by which s is sorted."
    import re

    return map(try_int, re.findall(r'(\d+|\D+)', s))


def natcmp(a, b):
    "Natural string comparison, case sensitive."
    return cmp(natsort_key(a), natsort_key(b))


def natcasecmp(a, b):
    "Natural string comparison, ignores case."
    return natcmp(a.lower(), b.lower())


def natsort(seq, cmp=natcmp):
    "In-place natural string sort."
    seq.sort(cmp)


def AverageSigmaSum(Values):
    Value = 0
    Average = 1. * sum(Values) / len(Values)

    SigmaSum = 0.
    for j in Values:
        SigmaSum += (j - Average) ** 2

    Sigma = math.sqrt(SigmaSum/ (len(Values)-1))
    return Average, Sigma, sum(Values)


def Garfield():
    print('''
             __ __
            ,;::\::\\
          ,'/' `/'`/
      _\,: '.,-'.-':.
     -./"'  :    :  :\/,
      ::.  ,:____;__; :-
      :"  ( .`-*'o*',);
       \.. ` `---'`' /
        `:._..-   _.'
        ,;  .     `.
       /"'| |       \\
      ::. ) :        :
      |" (   \       |
      :.(_,  :       ;
       \\'`-'_/      /
        `...   , _,'
         |,|  : |
         |`|  | |
         |,|  | |
     ,--.;`|  | '..--.
    /;' "' ;  '..--. ))
    \:.___(___   ) ))'
           SSt`-'-''  
''')


def Penrose():
    print('''
     ____  ____  ____  ____
    /\   \/\   \/\   \/\   \              
   /  \___\ \___\ \___\ \___\             
   \  / __/_/   / /   / /   /             
    \/_/\   \__/\/___/\/___/              
      /  \___\    /  \___\                
      \  / __/_  _\  /   /                
       \/_/\   \/\ \/___/                 
         /  \__/  \___\                   
         \  / _\  /   /                   
          \/_/\ \/___/                    
            /  \___\                      
            \  /   /                      
             \/___/        
''')


def RenameFile(Source, Destination):
    if (platform.system() == "Windows"):
        import ctypes

        ctypes.windll.kernel32.MoveFileExW(Source, Destination, 0x1)
        time.sleep(1)
    else:
        os.rename(Source, Destination)


def update(orig_dict, new_dict, AppendToLists = False):
    for key, val in new_dict.items():
        if isinstance(val, collections.Mapping):
            tmp = update(orig_dict.get(key, {}), val)
            orig_dict[key] = tmp
        elif AppendToLists and isinstance(val, list):
            orig_dict[key] = orig_dict.get(key, []) + val
        else:
            orig_dict[key] = new_dict[key]
    return orig_dict


def RemFPWindowFunction(FPFrequency, DataX, DataYOriginal=[]):
    DataY = []
    i2 = 0
    for i in DataX:
        Sign = 1
        if i < 0:
            Sign = -1
        Factor = 1.
        if abs(i) > FPFrequency * 0.85 and abs(i) < FPFrequency * 1.15:
            # Factor = EMPyLib.Fitting.Lorentzian(i,[FPFrequency*0.05,Sign*FPFrequency,-1,1])
            Factor = 0
        if len(DataYOriginal):
            DataY.append(Factor * DataYOriginal[i2])
        else:
            DataY.append(Factor)
        i2 += 1
    return np.array(DataY)


PointMarkers = [
    'o',  # circle marker
    's',  # square marker
    'p',  # pentagon marker
    '*',  # star marker
    'h',  # hexagon1 marker
    'H',  # hexagon2 marker
    '+',  # plus marker
    'x',  # x marker
    'D',  # diamon
    'v',  # triangle_down marker
    '^',  # triangle_up marker
    '<',  # triangle_left marker
    '>',  # triangle_right marker
    '1',  # tri_down marker
    '2',  # tri_up marker
    '3',  # tri_left marker
    '4',  # tri_right marker
]
def GetPointMarker(i):
    return PointMarkers[i%len(PointMarkers)]

PlotColors = [
    '#348ABD', '#7A68A6', '#A60628', '#467821', '#CF4457', '#188487', '#E24A33'
    # E24A33 : orange
    # 7A68A6 : purple
    # 348ABD : blue
    # 188487 : turquoise
    # A60628 : red
    # CF4457 : pink
    # 467821 : green
]


def ExtractMultiParameterComsolAbfallData(Data):
    MultiParameterData = [

    ]
    if Data.has_key('x') and Data.has_key('y'):
        ParameterIndex = 0
        ParameterValue = 0
        if Data.has_key('ParameterValue') and len(Data['ParameterValue']):
            ParameterValue = Data['ParameterValue'][0]
        MultiParameterData.append({
            'x': [],
            'y': [],
            'ParameterValue': ParameterValue,
        })
        for j in range(len(Data['x'])):
            if Data.has_key('ParameterValue') and j > 0 and abs(
                            Data['ParameterValue'][j] - Data['ParameterValue'][j - 1]) / (
            Data['ParameterValue'][j]) > 1e-4:
                MultiParameterData.append({
                    'x': [],
                    'y': [],
                    'ParameterValue': Data['ParameterValue'][j],
                })
                ParameterIndex += 1
            elif not Data.has_key('ParameterValue') and j > 0 and abs(Data['x'][j] - Data['x'][j - 1]) / (
            Data['x'][j]) > 1e-2:
                MultiParameterData.append({
                    'x': [],
                    'y': [],
                    'ParameterValue': 0,
                })
                ParameterIndex += 1
            else:
                MultiParameterData[ParameterIndex]['x'].append(Data['x'][j])
                MultiParameterData[ParameterIndex]['y'].append(Data['y'][j])
    return MultiParameterData


def MergeData(DataArray):
    NewData = {
        'x': [],
        'y': []
    }
    DataXArray = []
    DataYArray = []
    for Data in DataArray:
        DataXArray.append(Data[0])
        DataYArray.append(Data[1])

    SortedData = np.transpose(
        sorted(np.transpose(
            np.array(
                [np.hstack(DataXArray), np.hstack(DataYArray)])
        ),
            key=lambda x: x[0]
        )
    )
    NewData['x'] = SortedData[0]
    NewData['y'] = SortedData[1]
    return NewData


def SaveMatplotlibFigureAsPickle(Figure, Path):
    Filename = os.path.basename(Path)
    FolderPath = os.path.dirname(Path)
    FilenameNoSuffix, Suffix = os.path.splitext(Filename)

    f = open(FolderPath + '/' + FilenameNoSuffix + '.pickle', 'w')
    ax = Figure.gca()
    pickle.dump(ax, f)
    f.close()
    f = open(FolderPath + '/' + FilenameNoSuffix + '.py', 'w')
    f.write('''
#!/usr/bin/python
import matplotlib.pyplot as plt
import pickle
ax = pickle.load(file("''' + FilenameNoSuffix + '''.pickle"))
plt.show()
''')
    # os.fchmod(f, 0766)

    f.close()


def reglob(path, exp, invert=False):
    """glob.glob() style searching which uses regex

    :param exp: Regex expression for filename
    :param invert: Invert match to non matching files
    """

    m = re.compile(exp)

    if invert is False:
        res = [f for f in os.listdir(path) if m.search(f)]
    else:
        res = [f for f in os.listdir(path) if not m.search(f)]

    res = map(lambda x: "%s/%s" % (path, x,), res)
    return res


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

try:
    from builtins import input
except ImportError as e:
    input = raw_input
