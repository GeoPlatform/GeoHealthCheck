import sys

from pyquery import PyQuery
from GeoHealthCheck.plugin import Plugin
from GeoHealthCheck.check import Check
try:
    from html import escape  # python 3.x
except ImportError:
    from cgi import escape  # python 2.x

#-# imported for this plugin #-#
# import models
import requests
import os
import urllib
import re
# from owslib.etree import etree
from pdb import set_trace as bp
import traceback

""" Contains basic Check classes for a Probe object."""


class SlaOGCTestValidation(Check):
    """
    Leverages the TEAM Engine project API to programatically test a service.

    @see: 
        http://opengeospatial.github.io/teamengine/index.html
        https://github.com/opengeospatial/teamengine
    """

    NAME = 'Runs tests in TEAM Engine test software. '
    DESCRIPTION = 'Test the service for validation '

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
        'Frequency': {
            'type': 'string',
            'description': 'How often should we run tests to check compliance?',
            'default': 'Every 3 Days',
            'required': True,
            'range': ['Every 1 Day', 
                    'Every 3 Days', 
                    'Every 1 Week', 
                    'Every 2 Weeks', 
                    'Every 1 Month']
        },
        'Time': {
            'type': 'string',
            'description': 'What time should we run the test?',
            'default': '3:00AM',
            'required': True,
            'range': ['12:00PM', 
                    '1:00AM',
                    '2:00AM',
                    '3:00AM',
                    '4:00AM',
                    '5:00AM',
                    '6:00AM',
                    '7:00AM',
                    '8:00AM']
        }
    }
    """Param defs"""

    def __init__(self):
        Check.__init__(self)

    def perform(self):
        # Wait until time matches -- Don't do now...
        # Log in (or register) to TEAM Engine server

        # Call to TEAM Engine to run test
        try :

            ##### For Testing (from file) #####
            # lines = [];
            # file = open(os.path.dirname(__file__) + "/../../../../results.xml")
            # for line in file:
            #     lines.append(line)
            # 
            # text = ''.join(lines).rstrip()
            # self.set_result(True, text)
            ###################################

            ############ The Real deal ########
            te_test_endpoint = self.get_param('TEAM Engine endpoint')
            te_test_name = self.get_param('Test to Run')
            te_test_params = re.match(".+\[(.+)\]", te_test_name).groups()[0]
            
            # Must URL encode '&' chars per TEAM Engine documentation : 
            #   http://opengeospatial.github.io/teamengine/users.html
            resource_endpoint = self.probe.response.url.replace('&','%26')

            try:
                url = ("%s/rest/suites/%s/run?wfs=%s" % (te_test_endpoint, te_test_params, resource_endpoint)).replace('//rest','/rest')
                cleanUrl = url.replace('https', 'http').replace('//rest','/rest')
                print cleanUrl
                resp = requests.get(cleanUrl)
                text = resp.text

                # If the test ran without issue
                if resp.status_code == requests.codes.ok:
                    doc = PyQuery(text.encode())
                    failed = int(doc.attr('failed'))

                    # report a pass or a fail
                    if failed > 0 :
                        self.set_result(False, text)
                    else :
                        self.set_result(True, text)

                # Error happened running test
                else:
                    print text
                    self.set_result(False, text)

            except Exception as err:
                print err
                traceback.print_stack()
                self.set_result(False, err)
                return
            ###################################

            # bp()



        except Exception as err: 
            print(err)
            self.set_result(False, err)


# ASSUMPTION: this assumes that there is an hourly (or ever so often) check being run....
class SlaVerifyUptime(Check):
    """
    Things
    """

    NAME = 'Verify service reliability meets minimum requirements.'
    DESCRIPTION = 'Verify that service has been avaliable at a given minimum percentage rate.'

    PARAM_DEFS = {
        'Minimum Uptime': {
            'type': 'string',
            'description': 'What is the minumum up-time percentage.',
            'default': '75%',
            'required': True,
            'range': [ '98%', '95%', '90%', '85%', '80%', '75%', '70%', '65%', '60%', '55%', '50%' ]
        }
    }
    """Param defs"""

    def __init__(self):
        Check.__init__(self)

    def perform(self):
        # self.probe._resource.identifier
        reliability = self.probe._resource.reliability
        min_rel = int(str(self._parameters['Minimum Uptime']).replace('%',''))

        if reliability < min_rel :
            self.set_result(False, "Service did not meet minimum SLA uptime requirement")
      


class SlaPreformant(Check):
    """
    Things
    """

    NAME = 'Verify service preformance.'
    DESCRIPTION = '{ Verify that is preformant... }'

    PARAM_DEFS = {
        'PARAM?': {
            'type': 'string',
            'description': '{ What params??? }',
            'default': None,
            'required': True,
            'range': None
        }
    }
    """Param defs"""

    def __init__(self):
        Check.__init__(self)

    def perform(self):
        result = True
        msg = 'OK'
        self.set_result(result, msg)


    # ASSUMPTION: this assumes that there is an hourly (or ever so often) check being run....

    # get record of uptime...
    # get average
    # see if its above the given average...


class SLATestResultsHelper(object):
    """
    Helper class for reading and manipulating Test results saved from TEAM Engine
    test suite runs.
    """

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