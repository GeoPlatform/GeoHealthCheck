# -*- coding: utf-8 -*-

# tmp: test workround for loading from this file
# import sys
# sys.path.insert(0,'/Users/forestg/dev/OGC/GeoHealthCheck')

from GeoHealthCheck.probe import Probe
from GeoHealthCheck.result import Result

from owslib.wms import WebMapService
from owslib.wfs import  WebFeatureService
# from pyquery import PyQuery

import requests
import os
import random
import re
import datetime
import time
import zipfile


# User managment
from GeoHealthCheck.models import User

# For debugging
from pdb import set_trace as bp
import traceback


### Abstract Test Probe ###
class SLA_Compliance(Probe):
    """
    SLA_Compliance:
        This runs tests against the OGC Test Engine server to verify resource
        compliance with standards.
    """
    NAME = 'OGC Standards Compliance Test'
    DESCRIPTION = 'Check for resource compliance against OGC standards test.'
    AUTHOR = 'ImageMattersLLC Team'
    # See enums.py for complete list
    RESOURCE_TYPE = '*:*'

    REQUEST_METHOD = 'GET'

    PARAM_DEFS = {
        'TEAM Engine endpoint': {
            'type': 'string',
            'description': 'URL endpoint for the TEAM Engine service',
            'default': 'http://cite.opengeospatial.org/te2/',
            'required': True,
            'range': [  'http://cite.opengeospatial.org/te2/']
                        # 'http://teamengine:8080/teamengine/',
                        # 'http://cite.opengeospatial.org/teamengine/',
                        # 'http://localhost:8088/teamengine/']
                      
                        
        },
        'Test to Run': {
            'type': 'string',
            'description': 'What test would you like to run?',
            'default': 'WFS 2.0 (ISO 19142:2010) Conformance Test Suite [wfs20/1.26]',
            'required': True,
            'range': [
                'WFS 2.0 (ISO 19142:2010) Conformance Test Suite [wfs20/1.26]',
                'Conformance Test Suite - OGC Web Map Service 1.3.0 [wms/1.23]',
                'GML (ISO 19136:2007) Conformance Test Suite, Version 3.2.1 [gml32/1.25]',
                'OGC Catalogue 3.0 Conformance Test Suite [cat30/1.0]'
                ]
                # 'Conformance Test Suite - OGC Web Map Service 1.1 [wms/1.16]',
                # 'Conformance Test Suite - OGC Web Feature Service 1.0.0 [wfs/1.12]',

                # 'ets-sensorml20 [sensorml20/0.6]'
                # 'OWS Context 1.0 Conformance Test Suite [owc10/0.1]',
                # 'OGC KML 2.x Conformance Test Suite [kml2/0.5]', 
                # 'KML 2.2 Conformance Test Suite [kml22/1.12]',

                # 'SensorThings API (STA) [sta10/1.0]',
                # 'GeoPackage 1.2 Conformance Test Suite [gpkg12/0.1]',
                # 'GeoPackage 1.0 Conformance Test Suite [gpkg10/1.0]',
        }
    }

    CHECKS_AVAIL = {
        'GeoHealthCheck.plugins.check.slachecks.SlaOGCTestValidation': {
            'default': True
        }
    }

    def __init__(self):
        Probe.__init__(self)


    def perform_request(self):

        # owner = User.query.filter_by(username=uname).first() 

        ######### Run the Test #########
        result = Result(False, 'Test failed to run')
        result.start() # start the timer

        ############ The Real deal ############
        try:
            # Register user if they have not already been registerd in TE 
            # api = TeamEngineAPI(self.get_param('TEAM Engine endpoint'))
            # api.register(owner.username, owner.password)
            # api.authenticate(owner.username, owner.password)

            te_test_endpoint = self.get_param('TEAM Engine endpoint')
            te_test_name = self.get_param('Test to Run')
            te_test_params = re.match(".+\[(.+)\]", te_test_name).groups()[0]
        
            # Must URL encode '&' chars per TEAM Engine documentation : 
            #   http://opengeospatial.github.io/teamengine/users.html
            resource_endpoint = self._resource.url.replace('&','%26')
        

            # Get the test param matched to the test being run
            def get_param(test):
                switcher = {
                    'wms/1.16': 'capabilities-url',
                    'wms/1.23': 'capabilities-url',
                    'wfs/1.12': 'capabilities-url',
                    'wfs20/1.26': 'wfs',
                    'gml32/1.21': 'gml',
                    'kml2/0.5': 'kml'
                }
                # Others will return default for these
                return switcher.get(test, 'iut') # With a default


            url = ("%s/rest/suites/%s/run?%s=%s" % (te_test_endpoint, \
                                                    te_test_params, \
                                                    get_param(te_test_params),\
                                                    resource_endpoint))
            cleanUrl = url.replace('https', 'http').replace('//rest','/rest')
            print cleanUrl

            headers = { 'Accept' : 'application/zip' }

            resp = requests.get(cleanUrl, headers=headers)
            print(resp.status_code)
            print(resp)
            

            # Save response zip to file
            uname = self._resource.owner_identifier
            resource_id = self._resource.identifier

            file_name = uname + '_' + str(resource_id) + "_" + str(time.time())

            # Allow path to be passed in
            path = os.environ['STATIC_HOME'] + file_name

            with open(path + '.zip', 'wb') as f:
                f.write(resp.content)

            # Go ahead and unzip in static directory to serve (HTTP)
            zip = zipfile.ZipFile(path + '.zip', 'r')
            zip.extractall(path)
            zip.close()

            # print resp.content
            self.response = resp
            result.set_test_xml(file_name)
            result.set(True, "Test run successfully")

        except requests.ConnectionError as err:
            msg = "Error connecting to TeamEngine service at:  [" + te_test_endpoint + "]"
            print msg
            result.set(False, msg)
        except zipfile.BadZipfile as err:
            msg = "Invalid Zip file returned from TeamEngine server"
            print msg
            result.set(False, msg)
        except Exception as err:
            print(type(err))
            print(err)
            traceback.print_stack()
            result.set(False, "Error: " + str(err))

        result.stop()
        self.result.add_result(result)
        ###################################



#################### Concrete test probes ####################

### WFS concrete probe ####
class SLA_Compliance_WFS(SLA_Compliance):
    NAME = 'OGC Standards Compliance Test (WFS)'
    DESCRIPTION = 'Check for resource compliance against OGC WFS standards test.'
    AUTHOR = 'ImageMattersLLC Team'
    # See enums.py for complete list
    RESOURCE_TYPE = 'OGC:WFS'

    REQUEST_METHOD = 'GET'

    PARAM_DEFS = {
        'TEAM Engine endpoint': {
            'type': 'string',
            'description': 'URL endpoint for the TEAM Engine service',
            'default': 'http://cite.opengeospatial.org/te2/',
            'required': True
        },
        'Test to Run': {
            'type': 'string',
            'description': 'What test would you like to run?',
            'default': 'WFS 2.0 (ISO 19142:2010) Conformance Test Suite [wfs20/1.26]',
            'required': True
        }
    }  


#### WMS concrete probe ####
class SLA_Compliance_WMS(SLA_Compliance):
    NAME = 'OGC Standards Compliance Test (WMS)'
    DESCRIPTION = 'Check for resource compliance against OGC WMS standards test.'
    AUTHOR = 'ImageMattersLLC Team'
    # See enums.py for complete list
    RESOURCE_TYPE = 'OGC:WMS'

    REQUEST_METHOD = 'GET'

    PARAM_DEFS = {
        'TEAM Engine endpoint': {
            'type': 'string',
            'description': 'URL endpoint for the TEAM Engine service',
            'default': 'http://cite.opengeospatial.org/te2/',
            'required': True
        },
        'Test to Run': {
            'type': 'string',
            'description': 'What test would you like to run?',
            'default': 'Conformance Test Suite - OGC Web Map Service 1.3.0 [wms/1.23]',
            'required': True
        }
    }    


#### CWS (Catalogue Conformance) Concrete Probe ####
class SLA_Compliance_CSW(SLA_Compliance):
    NAME = 'OGC Standards Compliance Test (WMS)'
    DESCRIPTION = 'Check for resource compliance against OGC CSW standards test.'
    AUTHOR = 'ImageMattersLLC Team'
    # See enums.py for complete list
    RESOURCE_TYPE = 'OGC:CSW'

    REQUEST_METHOD = 'GET'

    PARAM_DEFS = {
        'TEAM Engine endpoint': {
            'type': 'string',
            'description': 'URL endpoint for the TEAM Engine service',
            'default': 'http://cite.opengeospatial.org/te2/',
            'required': True
        },
        'Test to Run': {
            'type': 'string',
            'description': 'What test would you like to run?',
            'default': 'OGC Catalogue 3.0 Conformance Test Suite [cat30/1.0]',
            'required': True
        }
    }  




"""
    SLA_Preformance General Rules:
    Tests a resource to make sure it meets minimum preformance requirements

    Standards are set as following:
    - Initial Response : max time 3 Seconds
    - 470 Kilobytes image (e.g. 800 × 600 color 8 bits): max time 5 seconds
    - Download Service Metadata operation: max time 10 seconds
    - Get Spatial Data Set/Get Spatial Object
        - initial response: max 30 seconds
        - maintain : 500 Spatial Objects per second
    - Describe Spatial Data Set/Describe Spatial Object Type
        - initial response: max 10 seconds
        - maintain 500 descriptions of Spatial Objects per second
"""


"""
SLA_Avalability:

Run tests to make sure resource meets minimum uptime requirements.

Standards are set as following:
    - Initial Response : max time 3 Seconds
"""
class SLA_Avalability(Probe):
    NAME = 'SLA Avaliability Probe'
    DESCRIPTION = 'Check for resource meets minimum uptime requirements.'
    AUTHOR = 'ImageMattersLLC Team'

    # See enums.py for complete list
    RESOURCE_TYPE = '*:*'

    REQUEST_METHOD = 'GET'

    # PARAM_DEFS = {}

    CHECKS_AVAIL = {
        'GeoHealthCheck.plugins.check.checks.HttpStatusNoError': {
            'default': True
        },
        'GeoHealthCheck.plugins.check.slachecks.UnderMaxResponseTime': {
            'default': True,
        },
        'GeoHealthCheck.plugins.check.slachecks.SlaVerifyUptime': {
            'default': True,
        }
    }

    def __init__(self):
        Probe.__init__(self)



"""
SLA_image_preformance:

Check to make sure a WMS image resource retrevial is preformant 
for a service.

Standards are set as following:
    - 470 Kilobytes image (e.g. 800 × 600 color 8 bits): max time 5 seconds
"""
class SLA_image_preformance(Probe):

    NAME = 'SLA Image Download Preformance'
    DESCRIPTION = 'Check WMS image download preformance.'
    AUTHOR = 'ImageMattersLLC Team'

    # See enums.py for complete list
    RESOURCE_TYPE = 'OGC:WMS' # Could possibly expand at some point

    REQUEST_METHOD = 'GET'

    # PARAM_DEFS = {}

    CHECKS_AVAIL = {
        # Do not include "HttpStatusNoError" as we do not actually set a
        # request (we )
        'GeoHealthCheck.plugins.check.slachecks.UnderMaxResponseTime': {
            'default': True,
        }
    }

    def __init__(self):
        Probe.__init__(self)


    def perform_request(self):

        ######### Run the Test #########
        result = Result(True, 'Ok')
        result.start() # start the timer

        ############ The Real deal ############
        try:
            wms = WebMapService(self._resource.url, version='1.3.0')
            layers = list(wms.contents) # list of layers
        
            # Request image and check will make sure it happened in time
            wms.getmap(layers=layers, # Pull all layers
                srs='EPSG:4326',
                bbox=(-112, 36, -106, 41),
                size=(800, 600),
                format='image/jpeg',
                transparent=True)

            # layer = wms[random.choice(layers)] # Random Layer
                # styles=[layer.styles.keys()[0]],

        except Exception as err:
            print err
            traceback.print_stack()
            result.set(False, err)
        
        result.stop()
        self.result.add_result(result)


# class SLA_Capacity(Probe):
    # NOT yet implemented








###############################################################################


"""
Helper class for reading and manipulating Test results saved from TEAM Engine
test suite runs.
"""
class SLATestResultsHelper(object):

    def __init__(self, name):
        self.NAME = name

    # Credit:
    # http://code.activestate.com/recipes/577027-find-file-in-subdirectory/
    def findInSubdirectory(self, filename, subdirectory=''):
        if subdirectory:
            path = subdirectory
        else:
            path = os.getcwd()
        for root, dirs, names in os.walk(path):
            if filename in names:
                return os.path.join(root, filename)
        raise 'File not found'

    # Get index.html path from the static serve site (for HTML display)
    def get_index(self):
        full_path = os.environ['STATIC_HOME'] + self.NAME if self.NAME else ''
        return re.sub(r'^.+/static', '/static', self.findInSubdirectory('index.html', full_path))
        
    # Get index.html with full path (for system processing)
    def get_index_full_path(self):
        full_path = os.environ['STATIC_HOME'] + self.NAME if self.NAME else ''
        return self.findInSubdirectory('index.html', full_path)

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
        # NOTE: we do not save cookie after registration as it prevents 
        # immediate login
        return requests.post(self.ENDPOINT + 'registrationHandler', \
                    data=payload, \
                    cookies=self.COOKIEJAR)

    def authenticate(self, uname, password):
        payload = (('j_username', uname),('j_password', password))
        resp = requests.post(self.ENDPOINT + 'j_security_check', \
                        data=payload, \
                        cookies=self.COOKIEJAR)
        self.saveCookies(resp)
        return resp

    """
    Return format:
        [('{Test name}', '{etsCode}/{etsVersion}'),...]
    Example:
        [('GML (ISO 19136:2007) Conformance Test Suite, Version 3.2.1', 
            'gml32/1.23'),...]
    """
    def getAvailableTests(self):
        resp = requests.get(self.ENDPOINT + 'rest/suites')

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