import collections

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


try:
    from builtins import input
except ImportError as e:
    input = raw_input
