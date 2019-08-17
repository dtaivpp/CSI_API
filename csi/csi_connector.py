import requests
from csi.api_errors import ApiError

class CsiConnector:
  """
  CSI Connector
  ~~~~~~~~~~~~~

  CSI Connector is a helper class to simplify communicating with the Virtual Observer / CSI API
  
  Basic Get Useage:
    >>> baseURL = "https://cloud.csiworld.com/VOWebAPI/v5/"
    >>> csi = CsiConnector(token, baseURL)
    >>> params = {'filter': 'f.FName|o.eq|v.Tippett',
                  'fields': 'FName, LName',
                  'perpage':100}
    >>> data = csi.query(Endpoints.AgentInfo, params)
  

  Basic Post Useage:
    >>> baseURL = "https://cloud.csiworld.com/VOWebAPI/v5/"
    >>> csi = CsiConnector(token, baseURL)
    >>> data = {'User': 'jsmith', 'Function': 'Pause'}
    >>> csi.query(Endpoints.lightstout, data)

  :copyright: (c) 2019 by David Tippett.
  :license: MIT License, see LICENSE for more details.
  """
  def __init__(self, token, baseURL):
    self._baseURL = baseURL
    self._headers = {
      'ApiToken': token,
      'Accept': "application/json",
      'Content-Type': "application/json",
      'Accept-Encoding': "gzip, deflate"
    } 


  def _check_status_error(self, status_code, endpoint):
    """checks the return status code"""
    if status_code != 200 and status_code != 201:
      if endpoint != None:
        raise ApiError('{} to {} returned {}'.format(endpoint['type'], endpoint['endpoint'], status_code)) 
      else:
        raise ApiError('Request returned {}'.format(status_code)) 
    pass


  def _getNext(self, _url):
    """_getNext is used to get the next url in a sequence
    """
    
    result = requests.get(_url, headers=self._headers)
    self._check_status_error(result.status_code, None)

    return result.json()


  # The triple quotes create a doc string, so anytime you try and use the getData
  # function a dialog will pop up and show you what it is and what it expects
  # Underscores help us see which variables are local to the getData function
  def _get_initial(self, endpoint, parameters):
    """ _getInitial calls the endpoint the first time and returns the json body
    """
    
    # Generating the url using the endpoint and base url 
    url = self._baseURL + endpoint['endpoint']
    
     
    resp =  requests.get(
      url,
      params=parameters,
      headers=self._headers
    )

    self._check_status_error(resp.status_code, endpoint)

    return resp.json()


  def _post(self, endpoint, parameters):
    r"""
    _post is used to post data to the API endpoint 

    Parameters: 
        endpoint: Endpoint object obtained from endpoints helper class 
        paramaters: data to be sent 
    """


    resp = requests.post(
      self._baseURL + endpoint['endpoint'], \
      data=parameters, \
      headers=self._headers
    )

    self._check_status_error(resp.status_code, endpoint)

    return resp


  def query(self, endpoint, parameters):
    r"""
    Forms either get or post query request to Five9 API 
 
    :endpoint: endpoint object obtained from endpoints helper class
    :parameters: either json data to post or parameters object for get request
    """
    if endpoint['type'] == "get":
      _return = self._get_initial(endpoint, parameters)
      _data = _return[endpoint['datatag']]

      # Check if data has a next
      while _return["NextPageUri"] != None:
        _return = self._getNext(_return["NextPageUri"])

        _data.extend(_return[ endpoint['datatag']])
      
      return _data
    
    else:
      _return = self._post(endpoint, parameters)
      print()



class Endpoints:
  """
  Helper class with Endpoint / Datatag / Protocol 
  Used to prevent spelling errors
  """
  #### Get Endpoints ####

  # Agents #
  AgentInfo = {'endpoint':"Agents/AgentInfo", 'datatag':"AgentsInfo", 'type': "get"}
  AgentType = {'endpoint':"Agents/AgentType", 'datatag': "AgentTypes", 'type': "get"}
  AgentSupervisor = {'endpoint': "Agents/Supervisor",'datatag':"Supervisors", 'type': "get"}
  
  # Evaluations #
  EvaluationEvaluator = {'endpoint': "Evaluations/Evaluator", 'datatag': "Evaluators", 'type': "get"}
  EvaluationAssignment = {'endpoint': "Evaluations/Assignment", 'datatag': "Assignments", 'type': "get"}
  EvaluationReview = {'endpoint': "Evaluations/Review", 'datatag': "Reviews", 'type': "get"}
  EvaluationScoringSession = {'endpoint': "Evaluations/ScoringSession", 'datatag': "ScoringSessions", 'type': "get"}
  EvaluationSurvey = {'endpoint': "Evaluations/Survey", 'datatag': "Surveys", 'type': "get"}

  # Recordings #
  RecordedEvent = {'endpoint': "Recordings/RecordedEvent", 'datatag': "RecordedEvents", 'type': "get"}

  # Speech Analytics #
  SpeechTranscription = {'endpoint': "SpeechAnalytics/Transcription", 'datatag': "Transcriptions", 'type': "get"}
  SpeechDiscovery = {'endpoint': "SpeechAnalytics/Discovery", 'datatag': "Discoveries", 'type': "get"}

  # Admin #
  AdminUser = {'endpoint': "Admin/User", 'datatag': "Users", 'type': "get"}
  AdminProfile = {'endpoint': "Admin/Profile", 'datatag': "Profiles", 'type': "get"}


  #### Post Endpoints ####
  
  # Value Added #
  ValueAdded = {'endpoint': "ValueAddedMetadata/Tag", 'type':"post"}

  # PCI #
  LightsOut = {'endpoint': "PCI/LightsOut", 'type': "post"}
  
  # Adherence #
  Adherence = {'endpoint': "Adherence/AgentState", 'type': "post"}

  # Recording Metadata #
  RecordingMetadata = {'endpoint': "RecordingMetadata/CallObject"}
