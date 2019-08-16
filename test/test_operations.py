import unittest
import sys
import os
import json
from unittest import mock
sys.path.insert(1,os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from csi import CsiConnector
from csi import Endpoints
from csi import ApiError

class BasicTests(unittest.TestCase):

  def _mock_response(
    self,
    status=200,
    content="CONTENT",
    json_data=None,
    raise_for_status=None):
    """
    since we typically test a bunch of different
    requests calls for a service, we are going to do
    a lot of mock responses, so its usually a good idea
    to have a helper function that builds these things
    """
    mock_resp = mock.Mock()
    # mock raise_for_status call w/optional error
    mock_resp.raise_for_status = mock.Mock()
    if raise_for_status:
        mock_resp.raise_for_status.side_effect = raise_for_status
    # set status code and content
    mock_resp.status_code = status
    mock_resp.content = content
    # add json data if provided
    if json_data:
        mock_resp.json = mock.Mock(
            return_value=json_data
        )
    return mock_resp

  
  @mock.patch('csi.csi_connector.requests.get')
  def test_query_get(self, mock_get):
    csi = CsiConnector("asld34576y11lfawsergli34tyweo324owc", 'https://cloud.csiworld.com/VOWebAPI/v5/')
    
    mock_return_headers = {
      'Accept': 'application/json', 
      'Accept-Encoding': 'gzip, deflate', 
      'ApiToken': 'asld34576y11lfawsergli34tyweo324owc', 
      'Content-Type': 'application/json'
      }


    mock_resp = self._mock_response(
      json_data = {
        'NextPageUri': None,
        'AgentsInfo': [{'FName':'David', 'LName':'Tippett'}]})
  
    mock_get.return_value = mock_resp

    params = {'filters': 'f.FName|o.eq|v.Tippett',
                  'fields': 'FName, LName',
                  'perpage':100}
    data = csi.query(Endpoints.AgentInfo, params)

     
    mock_get.assert_called_with(
      "https://cloud.csiworld.com/VOWebAPI/v5/Agents/AgentInfo", 
      headers=mock_return_headers,
      params=params
      )
    
    self.assertEqual(data, [{'FName':'David', 'LName':'Tippett'}])


  @mock.patch('csi.csi_connector.requests.get')
  def test_query_failed_get(self, mock_get):
    csi = CsiConnector("asld34576y11lfawsergli34tyweo324owc", 'https://cloud.csiworld.com/VOWebAPI/v5/')
    
    mock_resp = self._mock_response(
      status = 400
      )
  
    mock_get.return_value = mock_resp

    params = {'filters': 'FName|eq|Tippett',
                  'fields': 'FName, LName',
                  'perpage':100}

    with self.assertRaises(ApiError) as cm:
      csi.query(Endpoints.AgentInfo, params)

    self.assertEqual("get to Agents/AgentInfo returned 400", str(cm.exception))


  @mock.patch('csi.csi_connector.requests.post')
  def test_query_post(self, mock_post):
    pass


if __name__ == "__main__":
  unittest.main()