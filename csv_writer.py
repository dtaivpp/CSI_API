from datetime import datetime

def _contains_special_char(_check_str):
  special_char = ['\n', ',']
  return any(st in _check_str for st in special_char)

def process_row(_obj):
  temp_row = ""
  for key in _obj:
    if _contains_special_char(_obj[key]):
      temp_row += "\"" +_obj[key] + "\"" + ","
    else:
      temp_row += _obj[key] + ","

  return temp_row += "\n"

def export_csv(_data, parameters):
  """
  Export CSV
  ~~~~~~~~~~~~~

  Exports Flat Json to CSV File
  
  Basic Useage:
    >>> data = {'datapoint1': "data1", 'datapoint2': "data, two", 'datapoint3': "data3"}
    >>> export_csv(data, {'path':"C:\\DropLocation\\", 'filename':"csvFile", 'overwrite':False})

  :copyright: (c) 2019 by David Tippett.
  :license: MIT License, see LICENSE for more details.
  """

  if parameters['overwrite']:
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



