from CSI_Connector import CSI_Connector, endpoint_spec
from csv_writer import export_csv


# If name = main tells us run this function if this file is being called
# aka if you are in cmd and running "python CSI_API.py"
if __name__ == '__main__':
  token = ""
  CSI = CSI_Connector(token)

  # Fill out parameters to spec (Page 6-8 Api Handbook)
  params = {
    "filter":"f.LName|o.lk|v.Tippett",
    "fields": "LName",
    "perpage": 10
  }

  # We use the endpoints object to avoid spelling errors and simplify collection names
  # Add more endpoints through the endpoint_spec class in api writer 
  data = CSI.query(endpoint_spec.AgentInfo, params)

  #export the data to a csv
  export_csv(data, 'C:\\Users\\datipp\\Documents\\','TestData')


