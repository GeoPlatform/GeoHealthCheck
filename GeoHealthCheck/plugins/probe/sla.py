# -*- coding: utf-8 -*-
from GeoHealthCheck.probe import Probe
from GeoHealthCheck.result import Result

import requests
import os
import re

from pyquery import PyQuery

# User managment
from GeoHealthCheck.models import User

# For debugging
from pdb import set_trace as bp
import traceback

# tmp: test workround for loading from this file
# import sys
# sys.path.insert(0,'/Users/forestg/dev/OGC/GeoHealthCheck')

class SLA_Compliance(Probe):
    """
    SLA_Compliance:
        This runs tests against the OGC Test Engine server to verify resource
        compliance with standards.
    """
    AUTHOR = 'ImageMattersLLC Team'
    NAME = 'OGC Standards Compliance'
    DESCRIPTION = 'Check for resource compliance against OGC standards test.'
    # See enums.py for complete list
    RESOURCE_TYPE = '*:*'

    REQUEST_METHOD = 'GET'

    PARAM_DEFS = {
        'TEAM Engine endpoint': {
            'type': 'string',
            'description': 'URL endpoint for the TEAM Engine service',
            'default': 'http://cite.opengeospatial.org/teamengine/',
            'required': True,
            'range': None
        },
        'Test to Run': {
            'type': 'string',
            'description': 'What test would you like to run?',
            # 'default': 'OGC Catalogue 3.0 Conformance Test Suite [cat30/1.0]',
            'required': True,
            'range': ['OGC Catalogue 3.0 Conformance Test Suite [cat30/1.0]',
                    'GeoPackage 1.0 Conformance Test Suite [gpkg10/1.0]',
                    'SensorThings API (STA) [sta10/1.0]',
                    'WFS 2.0 (ISO 19142:2010) Conformance Test Suite [wfs20/1.26]',
                    'KML 2.2 Conformance Test Suite [kml22/1.12]',
                    'GML (ISO 19136:2007) Conformance Test Suite, Version 3.2.1 [gml32/1.25]']
        },
        # 'Frequency': {
        #     'type': 'string',
        #     'description': 'How often should we run tests to check compliance?',
        #     'default': 'Every 3 Days',
        #     'required': True,
        #     'range': ['Every 1 Day', 
        #             'Every 3 Days', 
        #             'Every 1 Week', 
        #             'Every 2 Weeks', 
        #             'Every 1 Month']
        # },
        # 'Time': {
        #     'type': 'string',
        #     'description': 'What time should we run the test?',
        #     'default': '3:00AM',
        #     'required': True,
        #     'range': ['12:00PM', 
        #             '1:00AM',
        #             '2:00AM',
        #             '3:00AM',
        #             '4:00AM',
        #             '5:00AM',
        #             '6:00AM',
        #             '7:00AM',
        #             '8:00AM']
        # }
    }

    CHECKS_AVAIL = {
        'GeoHealthCheck.plugins.check.slachecks.SlaOGCTestValidation': {
            'default': True
        }
    }

    def __init__(self):
        Probe.__init__(self)

    def perform_request(self):

        uname = self._resource.owner_identifier
        owner = User.query.filter_by(username=uname).first() 

        ######### Run the Test #########
        result = Result(False, 'Guilty till proven innocent')
        result.start() # start the timer

        ###### For Testing (from file) #####
        try :
            lines = [];
            file = open(os.path.dirname(__file__) + "/../../../../results.xml")
            for line in file:
                lines.append(line)

            text = ''.join(lines).rstrip()

            # Make our own mock for testing here!
            self.response = requests.Response
            self.response.text = text
            self.response.status_code = 200

            result.set(True, text)
        except Exception as err: 
            print(err)
            traceback.print_stack()
            result.set(False, err)
        finally:
            result.stop()
            self.result.add_result(result)
        ###################################

        ############ The Real deal ############
        # try:
        #     # Register user if they have not already been registerd in Team Engine  
        #     api = TeamEngineAPI(self.get_param('TEAM Engine endpoint'))
        #     api.register(owner.username, owner.password)
        #     api.authenticate(owner.username, owner.password)

        #     te_test_endpoint = self.get_param('TEAM Engine endpoint')
        #     te_test_name = self.get_param('Test to Run')
        #     te_test_params = re.match(".+\[(.+)\]", te_test_name).groups()[0]
        
        #     # Must URL encode '&' chars per TEAM Engine documentation : 
        #     #   http://opengeospatial.github.io/teamengine/users.html
        #     resource_endpoint = self._resource.url.replace('&','%26')
        
        
        #     url = ("%s/rest/suites/%s/run?wfs=%s" % (te_test_endpoint, te_test_params, resource_endpoint)).replace('//rest','/rest')
        #     cleanUrl = url.replace('https', 'http').replace('//rest','/rest')
  
        #     print cleanUrl

        #     resp = requests.get(cleanUrl)
        #     self.response = resp
        #     result.set(True, resp.text)
        #     bp()

        # except Exception as err:
        #     print err
        #     traceback.print_stack()
        #     result.set(False, err)
        
        # finally:
        #     result.stop()
        #     self.result.add_result(result)
        ###################################





class SLA_Avalability(Probe):
    """
    SLA_Avalability:
        Run tests to make sure resource meets minimum uptime requirements.
    """
    AUTHOR = 'ImageMattersLLC Team'
    NAME = 'Avaliability check'
    DESCRIPTION = 'Check for resource meets minimum uptime requirements.'
    # See enums.py for complete list
    RESOURCE_TYPE = '*:*'

    REQUEST_METHOD = 'GET'

    # PARAM_DEFS = {}

    CHECKS_AVAIL = {
        'GeoHealthCheck.plugins.check.checks.HttpStatusNoError': {
            'default': True
        }
    }

    def __init__(self):
        Probe.__init__(self)



# class SLA_Preformance(Probe):
#     """
#         SLA_Preformance:
#         Tests a resource to make sure it meets minimum preformance requirements

#         Standards are set as following:
#         - Initial Response : max time 3 Seconds
#          - 470 Kilobytes image (e.g. 800 × 600 color 8 bits): max time 5 seconds
#         - Download Service Metadata operation: max time 10 seconds
#         - Get Spatial Data Set/Get Spatial Object
#             - initial response: max 30 seconds
#             - maintain : 500 Spatial Objects per second
#         - Describe Spatial Data Set/Describe Spatial Object Type
#             - initial response: max 10 seconds
#             - maintain 500 descriptions of Spatial Objects per second
#     """
#     AUTHOR = 'ImageMattersLLC Team'
#     NAME = 'Preformace Check'
#     DESCRIPTION = 'Check for preformace measurement of a resource'
#     # See enums.py for complete list
#     RESOURCE_TYPE = '*:*'

#     REQUEST_METHOD = 'GET'

#     # PARAM_DEFS = {}

#     CHECKS_AVAIL = {
#         # ...
#     }

#     def __init__(self):
#         Probe.__init__(self)


# class SLA_Capacity(Probe):
    # NOT yet implemented








"""
Helper class for reading and manipulating Test results saved from TEAM Engine
test suite runs.
"""
class SLATestResultsHelper(object):

    def __init__(self, message):
        self.RESP = message
        try:
            self.DOC = PyQuery(self.RESP.encode())
        except Exception as err:
            print err
            self.DOC = None

    def is_xml_response(self):
        return self.DOC is not None

    def get_passes(self):
        if self.is_xml_response():
            return self.DOC.find('[status="PASS"]')
        else: 
            return []


    def get_failures(self):
        if self.is_xml_response():
            return self.DOC.find('[status="FAIL"]')
        else: 
            return []
        
    # Return default if empty
    def show(self, obj, other): 
        return obj if obj <> None else other  







"""
Helper class that allows for interacting with an OGC Team Engine server

Team Engine:
    http://opengeospatial.github.io/teamengine/
"""
class TeamEngineAPI(object):

    ENDPOINT = None
    UNAME = None
    password = None
    COOKIEJAR = None

    def __init__(self, endpoint):
        self.ENDPOINT = endpoint
        self.touch()

    def saveCookies(self, resp):
        self.COOKIEJAR = resp.cookies

    def touch(self):
        resp = requests.get(self.ENDPOINT + 'viewSessions.jsp')
        self.saveCookies(resp)

    def register(self, uname, password):
        payload = (('disclaimer', 'on'), \
                    ('username', uname), \
                    ('password', password), \
                    ('repeat_password', password))
        # NOTE: we do not save cookie after registration as it prevents immediate login
        return requests.post(self.ENDPOINT + 'registrationHandler', data=payload, cookies=self.COOKIEJAR)

    def authenticate(self, uname, password):
        payload = (('j_username', uname),('j_password', password))
        resp = requests.post(self.ENDPOINT + 'j_security_check', data=payload, cookies=self.COOKIEJAR)
        self.saveCookies(resp)
        return resp

    """
    Return format:
        [('{Test name}', '{etsCode}/{etsVersion}'),...]
    Example:
        [('GML (ISO 19136:2007) Conformance Test Suite, Version 3.2.1', 'gml32/1.23'),...]
    """
    def getAvailableTests(self):
        resp = requests.get(self.ENDPOINT + 'rest/suites')
        doc = PyQuery(resp.text.encode())

        yeah = []
        for r in doc('[href]'):
            yeah.append((r.text, r.get('id').replace('-','/')))
        return yeah

    # def runTest(self); # Run test as user... so we have a record of it

    # def listTestResults(self):

    # def getLatestTestResult(self):
    # self.listTestResults(self) #...
    # Will have to filter by somthing here.... 





######### Testing #########
# api = TeamEngineAPI('http://localhost:8088/teamengine/')
# print api.getAvailableTests()

# resp = api.register('newguy11', 'mypass11')
# print resp.text
# api.authenticate('forest1', 'forest12')
# print api.COOKIEJAR