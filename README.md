[![Build Status](https://travis-ci.com/dtaivpp/CSI_API.svg?branch=master)](https://travis-ci.com/dtaivpp/CSI_API)
[![BCH compliance](https://bettercodehub.com/edge/badge/dtaivpp/CSI_API?branch=master)](https://bettercodehub.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPi version](https://pypip.in/v/csi-tai/badge.png)](https://pypi.org/project/csi-tai/)

# Using the CSI API Library 

Please note this module was created in order to simplify bulk data pulling from the Virtual Observer API. This project is in no way affiliated with [CSI World / Virtual Observer](https://www.csiworld.com).

## Getting Started

To get started install the requests module using the following command.  

`python -m pip install csi-tai`


Basic Get Useage:  
  ```
  baseURL = "https://cloud.csiworld.com/VOWebAPI/v5"  
  csi = CsiConnector(token, baseURL)  
  params = {'filter': 'f.FName|o.eq|v.Tippett',  
                'fields': 'FName, LName',  
                'perpage':100}  
  data = csi.query(endpoints.AgentInfo, params)  
  ```

Basic Post Useage:  
  ```
  baseURL = "https://cloud.csiworld.com/VOWebAPI/v5"  
  csi = CsiConnector(token, baseURL)  
  data = {'User': 'jsmith', 'Function': 'Pause'}  
  csi.query(endpoints.lightstout, data)  
  ```
