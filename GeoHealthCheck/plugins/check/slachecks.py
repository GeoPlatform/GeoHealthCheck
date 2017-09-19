# -*- coding: utf-8 -*-
from GeoHealthCheck.plugin import Plugin
from GeoHealthCheck.check import Check
try:
    from html import escape  # python 3.x
except ImportError:
    from cgi import escape  # python 2.x

#-# imported for this plugin #-#
from pyquery import PyQuery
import datetime
import os
import requests

# User managment
from GeoHealthCheck.models import User

# For debugging
from pdb import set_trace as bp
import traceback
# tmp: test workround for loading from this file
# sys.path.insert(0,'/Users/forestg/dev/OGC/GeoHealthCheck')


"""
Leverages the TEAM Engine project API to programatically test a service.

@see: 
http://opengeospatial.github.io/teamengine/index.html
https://github.com/opengeospatial/teamengine
"""
class SlaOGCTestValidation(Check):

    NAME = 'Team Engine Test Compliance'
    DESCRIPTION = "Test resource against OGC's Team Engine"

    PARAM_DEFS = {
        # Tests to omit?
        # Something about not failing if test fails
    }
    """Param defs"""

    def __init__(self):
        Check.__init__(self)

    def perform(self):
        # uname = self.probe._resource.owner_identifier
        # owner = User.query.filter_by(username=uname).first()        

        # NOTE: This implementation will all change once
        # Team Engine get API endpoints for retrievig the data

        # If the test ran without issue
        if self.probe.response.status_code == requests.codes.ok:
            doc = PyQuery(self.probe.response.text.encode())
            failed = int(doc.attr('failed'))
    
            # report a pass or a fail
            if failed > 0 :
                self.set_result(False, self.probe.response.text )
            else :
                self.set_result(True, self.probe.response.text )
    
        # Error happened running test
        else:
            print self.probe.response.text
            self.set_result(False, self.probe.response.text )




"""
Check for verifying the uptime of a service
"""
class SlaVerifyUptime(Check):

    NAME = 'Verify service reliability meets minimum requirements (99.9%).'
    DESCRIPTION = 'Verify that service has been avaliable at a given minimum percentage rate.'

    PARAM_DEFS = {
        'Minimum Uptime': {
            'type': 'string',
            'description': 'What is the minumum up-time percentage.',
            'default': '90',
            'required': True,
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




"""
    SLA_Preformance:
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
UnderMaxResponseTime

Check to see if the probe response was under a maximum response time 
threshold.
"""
class UnderMaxResponseTime(Check):
    NAME = "Under maximum response time"
    DESCRIPTION = 'Check to see if a resource has responded under the ' \
                + 'maximun allowed responce time (in seconds)'

    PARAM_DEFS = {
        'Max Response Time (seconds)': {
            'type':'string',
            'description': 'What is the minumum up-time percentage.',
            'required': True,
            'range': [ '1','2','3','4','5','6','7','8','9','10' ]
        }
    }
    """Param defs"""

    def __init__(self):
        Check.__init__(self)

    def perform(self):
        try:
            start = self.probe.result.start_time
            if self.probe.result.end_time:
                end = self.probe.result.end_time
            else: 
                end = datetime.datetime.utcnow()

            # Elapse : respone time
            elapse = (end-start).total_seconds()

            # Target : Min resp time 
            max = int(str(self._parameters['Max Response Time (seconds)']))

            # print 'start: ' + str(start)
            # print 'end: ' + str(end) 
            # print 'elapse:' + str(elapse)
            # print 'max: ' + str(max)
            if elapse > max:
                result = False
                msg = 'Resource took too long to respond'
                self.set_result(result, msg)

        except Exception as err:
            print err
            traceback.print_stack()
            self.set_result(False, err)    

