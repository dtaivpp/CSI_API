from datetime import datetime

def contains_special_char(_check_str):
  special_char = ['\n', ',']
  return any(st in _check_str for st in special_char)

def process_row(_obj):
  temp_row = ""
  for key in _obj:
    if contains_special_char(_obj[key]):
      temp_row += "\"" +_obj[key] + "\"" + ","
    else:
      temp_row += _obj[key] + ","

  return temp_row += "\n"

def export_csv(_data, parameters):
  '''
  Exports Json List as csv

  Parameters: 
    Data (Json list data)
    Args Object = 
    {
      path: "C:\\Users\\Data\\",
      fileName: "MyCSV",
      overwrite: True/False (will append date and )
    }
      Path (Path to put file in)
      FileName (Name for file)
      Overwrite (true/false whether you want previous files overwritten)
        - Defaults to false
  '''


  if _overwrite:
    _path = parameters['path'] + parameters['filename'] + ".csv"
  else:
    now = datetime.now
    timestr = datetime.utcnow().strftime('%Y-%m-%d-%f')
    
    _path = parameters['path'] + parameters['filename'] + timestr + ".csv"

  _location = open(_path, 'w+')
  count = 0
  _filestr = ""

  header = _obj.keys()
  _filestr += process_row(header)

  for _obj in _data:
    _filestr += process_row(_obj)

  _location.write(_filestr)
  _location.close()



