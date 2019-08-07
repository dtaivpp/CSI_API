from datetime import datetime

def export_csv(_data, _path, _filename, _overwrite=False ):
  '''
  Exports Json List as csv

  Parameters: 
    Data (Json list data)
    Path (Path to put file in)
    FileName (Name for file)
    Overwrite (true/false whether you want previous files overwritten)
      - Defaults to false
  '''

  if _overwrite:
    _path = _path + _filename + ".csv"
  else:
    now = datetime.now
    timestr = datetime.utcnow().strftime('%Y-%m-%d-%f')
    
    _path = _path + _filename + timestr + ".csv"


  
  _location = open(_path, 'w+')
  count = 0
  _filestr = ""


  for _obj in _data:
    header = _obj.keys()

    if count == 0:
        for key in header:
          _filestr += key + ","
        
        _filestr += "\n"
        count += 1


    for key in _obj:
        _filestr += _obj[key] + ","

    _filestr += "\n"
    
  _location.write(_filestr)
  _location.close()