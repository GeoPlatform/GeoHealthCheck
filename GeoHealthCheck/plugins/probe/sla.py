import random

# tmp: test workround for loading from this file
import sys
sys.path.insert(0,'/Users/forestg/dev/OGC/GeoHealthCheck')

from GeoHealthCheck.probe import Probe
from GeoHealthCheck.result import Result
from owslib.wms import WebMapService

import traceback
import requests
import os
from pyquery import PyQuery
import re



class SLA(Probe):
    """
    Probe for WMS endpoint "drilldown": starting
    with GetCapabilities doc: get Layers and do
    GetMap on them etc. Using OWSLib.WebMapService.

    TODO: needs finalization.
    """
    AUTHOR = 'ImageMattersLLC Team'
    NAME = 'SLA Check'
    DESCRIPTION = 'Check for Compliance at a given Service Level Agreement (SLA).'
    # See enums.py for complete list
    RESOURCE_TYPE = '*:*'

    REQUEST_METHOD = 'GET'

    # PARAM_DEFS = {}

    CHECKS_AVAIL = {
        'GeoHealthCheck.plugins.check.checks.HttpStatusNoError': {
            'default': True
        },
        'GeoHealthCheck.plugins.check.slachecks.SlaOGCTestValidation': {
            'default': True
        },
        'GeoHealthCheck.plugins.check.slachecks.SlaVerifyUptime': {
            'default': True
        },
        # 'GeoHealthCheck.plugins.check.slachecks.SlaPreformant': {
        #     'default': True
        # }
    }
    """
    Checks avail for all specific Caps checks.
    Optionally override Check PARAM_DEFS using set_params
    e.g. with specific `value`.
    """

    def __init__(self):
        Probe.__init__(self)





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
        resp = requests.post(self.ENDPOINT + 'registrationHandler', data=payload, cookies=self.COOKIEJAR)
        self.saveCookies(resp)
        return resp

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
api = TeamEngineAPI('http://localhost:8088/teamengine/')
print api.getAvailableTests()

# resp = api.register('newguy11', 'mypass11')
# print resp.text
# api.authenticate('forest1', 'forest12')
# print api.COOKIEJAR