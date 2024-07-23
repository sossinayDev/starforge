import random as _r

vocals = ["a", "e", "i", "o", "u"]
consonants = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"]
all = vocals + consonants

most_probable = {}
mp_dict = {}


def _topfive(d):
    result = {}
    for item in d:
        


        '''
        d[item]
        >>> {'i': 725, 'n': 2086, 't': 1267, 'r': 1187, 'l': 711...}
        '''


        _tmplist = []
        _tmplist_vals = []
        for _item in d[item]:
            _tmplist.append(_item.lower())
            _tmplist_vals.append(d[item][_item])
        
        _tmplist_vals.sort(reverse=True)
        if len(_tmplist)>=5:
            _tmplist_vals=_tmplist_vals[0:5]

        _tmpresult = []

        for __item in _tmplist_vals:
            _tmpresult.append(_tmplist[_tmplist_vals.index(__item)])
        
        result[item] = _tmpresult
    return result

def init(dataset: str="datasets/data.txt"):
    global most_probable, mp_dict
    for _letter in all:
        most_probable[_letter]={}


    
    _TEXT = open(dataset, "r").read().lower()

    i=1
    for _letter in _TEXT:
        if len(_TEXT)>i:
            if _letter.lower() in all:
                if _TEXT[i].lower() in all:
                    try:
                        most_probable[_letter.lower()][_TEXT[i]]+=1
                    except:
                        most_probable[_letter.lower()][_TEXT[i]]=1                
        i+=1
    
    mp_dict = _topfive(most_probable)


def generate_name(lenght: int=_r.randint(3,10), capitalize: bool=False):
    global most_probable, mp_dict
    _startletter=_r.choice(all)
    if lenght == 1:
        return _startletter
    _name = _startletter
    _letter_before = _startletter
    for i in range(lenght-1):
        _letter_before= _r.choice(mp_dict[_letter_before])
        try:
            if not _name[-2] == _letter_before:
                _name += _letter_before
        except:
            _name += _r.choice(mp_dict[_letter_before])
    
    _name = _name[0].upper()+_name[1:len(_name)-1]
    if capitalize:
        return _name
    else:
        return _name.lower()