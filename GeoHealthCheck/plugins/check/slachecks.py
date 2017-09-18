from GeoHealthCheck.plugin import Plugin
from GeoHealthCheck.check import Check
try:
    from html import escape  # python 3.x
except ImportError:
    from cgi import escape  # python 2.x

#-# imported for this plugin #-#
from pyquery import PyQuery
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
        # 'Minimum Uptime': {
        #     'type': 'string',
        #     'description': 'What is the minumum up-time percentage.',
        #     'default': '75%',
        #     'required': True,
        #     'range': [ '98%', '95%', '90%', '85%', '80%', '75%', '70%', '65%', '60%', '55%', '50%' ]
        # }
    }
    """Param defs"""

    def __init__(self):
        Check.__init__(self)

    def perform(self):
        # self.probe._resource.identifier
        reliability = self.probe._resource.reliability
        # min_rel = int(str(self._parameters['Minimum Uptime']).replace('%',''))
        min_rel = 99.9

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

        # get record of uptime...
        # get average
        # see if its above the given average...
        # 
        self.set_result(result, msg)
