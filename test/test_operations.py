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
  csi = CsiConnector("asld34576y11lfawsergli34tyweo324owc", 'https://cloud.csiworld.com/VOWebAPI/v5/')
  mock_return_headers = {
    'Accept': 'application/json', 
    'Accept-Encoding': 'gzip, deflate', 
    'ApiToken': 'asld34576y11lfawsergli34tyweo324owc', 
    'Content-Type': 'application/json'
    }

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

    mock_resp = self._mock_response(
      json_data = {
        'NextPageUri': None,
        'AgentsInfo': [{'FName':'David', 'LName':'Tippett'}]})
  
    mock_get.return_value = mock_resp

    params = {'filters': 'f.FName|o.eq|v.Tippett',
                  'fields': 'FName, LName',
                  'perpage':100}
    data = self.csi.query(Endpoints.AgentInfo, params)
     
    mock_get.assert_called_with(
      "https://cloud.csiworld.com/VOWebAPI/v5/Agents/AgentInfo", 
      headers=self.mock_return_headers,
      params=params
      )
    
    self.assertEqual(data, [{'FName':'David', 'LName':'Tippett'}])


  @mock.patch('csi.csi_connector.requests.get')
  def test_query_failed_get(self, mock_get):
    
    mock_resp = self._mock_response(
      status = 400
      )
  
    mock_get.return_value = mock_resp

    params = {'filters': 'FName|eq|Tippett',
                  'fields': 'FName, LName',
                  'perpage':100}

    with self.assertRaises(ApiError) as cm:
      self.csi.query(Endpoints.AgentInfo, params)

    self.assertEqual("get to Agents/AgentInfo returned 400", str(cm.exception))


  @mock.patch('csi.csi_connector.requests.post')
  def test_query_post(self, mock_post):
    mock_resp = self._mock_response(
      status = 201
      )

    mock_post.return_value = mock_resp

    data = {'User': 'jsmith', 'Function': 'Pause'}
    self.csi.query(Endpoints.LightsOut, data)
    mock_post.assert_called_with(
      "https://cloud.csiworld.com/VOWebAPI/v5/PCI/LightsOut", 
      headers=self.mock_return_headers,
      data=data
      )

  @mock.patch('csi.csi_connector.requests.get')
  def test_get_next(self, mock_get):
    URL = "https://cloud.csiworld.com/VOWebAPI/v5/Evaluations/ScoringSession/?fields=HeaderKey&perpage=10&after=1289384092&pagenum=1"
    
    mock_resp = self._mock_response(
      status = 200
      )

    mock_get.return_value = mock_resp

    self.csi._getNext(URL)
    mock_get.assert_called_with(
      URL, 
      headers=self.mock_return_headers, 
    )


if __name__ == "__main__":
  unittest.main()