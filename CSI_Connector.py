import requests

class CSI_Connector:
  def __init__(self, token):
    self.baseURL = 'https://cloud66.csiworld.com/VOWebAPI/v5/'
    self._headers = {
      'ApiToken': token,
      'Accept': "application/json",
      'Content-Type': "application/json",
      'Host': "cloud66.csiworld.com",
      'Accept-Encoding': "gzip, deflate"
    } 


  def _getNext(self, _url):
    try:
      result = requests.get(_url, headers=self._headers)
    except:
      print(result.headers)

    return result.json()


  # The triple quotes create a doc string, so anytime you try and use the getData
  # function a dialog will pop up and show you what it is and what it expects
  # Underscores help us see which variables are local to the getData function
  def _getInitial(self, _endpoint, _parameters):
    '''
    query: Retrieves data from endpoint

    input: 
      endpoint (from endpoint spec)
      parameters (generated query string)
    '''
    
    # Generating the url using the endpoint and base url 
    url = self.baseURL + _endpoint['endpoint']
    
    try: 
      result =  requests.get(url, params = _parameters, headers=self._headers)
    except:
      print(result.headers)

    
    return result.json()


  def query(self, _endpoint, _parameters):
    _return = self._getInitial(_endpoint, _parameters)
    _data = _return[ _endpoint['datatag'] ]

    # Check if data has a next
    while _return["NextPageUri"] != None:
      _return = self._getNext(  _return["NextPageUri"] )

      _data.extend( _return[ _endpoint['datatag'] ] )
    
    return _data

class endpoint_spec:
  '''
  Data class with Endpoint / Datatag
  Used to prevent spelling errors
  '''
  #### Get Endpoints ####

  # Agents #
  AgentInfo = {'endpoint':"Agents/AgentInfo", 'datatag':"AgentsInfo"}
  AgentType = {'endpoint':"Agents/AgentType", 'datatag': "AgentTypes"}
  AgentSupervisor = {'endpoint': "Agents/Supervisor",'datatag':"Supervisors"}
  
  # Evaluations #
  EvaluationEvaluator = {'endpoint': "Evaluations/Evaluator", 'datatag': "Evaluators"}
  EvaluationAssignment = {'endpoint': "Evaluations/Assignment", 'datatag': "Assignments"}
  EvaluationReview = {'endpoint': "Evaluations/Review", 'datatag': "Reviews"}
  EvaluationScoringSession = {'endpoint': "Evaluations/ScoringSession", 'datatag': "ScoringSessions"}
  EvaluationSurvey = {'endpoint': "Evaluations/Survey", 'datatag': "Surveys"}

  # Recordings #
  RecordedEvent = {'endpoint': "Recordings/RecordedEvent", 'datatag': "RecordedEvents"}

  # Speech Analytics #
  SpeechTranscription = {'endpoint': "SpeechAnalytics/Transcription", 'datatag': "Transcriptions"}
  SpeechDiscovery = {'endpoint': "SpeechAnalytics/Discovery", 'datatag': "Discoveries"}

  # Admin #
  AdminUser = {'endpoint': "Admin/User", 'datatag': "Users"}
  AdminProfile = {'endpoint': "Admin/Profile", 'datatag': "Profiles"}
