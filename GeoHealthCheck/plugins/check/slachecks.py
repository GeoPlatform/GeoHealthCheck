import sys
# import views
import models

from pdb import set_trace as bp

from owslib.etree import etree
from GeoHealthCheck.plugin import Plugin
from GeoHealthCheck.check import Check
try:
    from html import escape  # python 3.x
except ImportError:
    from cgi import escape  # python 2.x

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
        'Frequency': {
            'type': 'string',
            'description': 'How often should we run tests to check compliance?',
            'default': 'Every 3 Days',
            'required': True,
            'range': [ 'Every 1 Day', 'Every 3 Days', 'Every 1 Week', 'Every 2 Weeks', 'Every 1 Month' ]
        },
        'Time': {
            'type': 'string',
            'description': 'What time should we run the test?',
            'default': None,
            'required': True,
            'range': ['1:00AM','2:00AM','3:00AM','4:00AM', '5:00AM', '6:00AM', '7:00AM', '8:00AM' ]
        },
        # 'Test name': {
        #     'type': 'string',
        #     'description': 'What time should we run the test?',
        #     'default': None,
        #     'required': True,
        #     'range': None
        # }
    }
    """Param defs"""

    def __init__(self):
        Check.__init__(self)

    def perform(self):
        result = True
        msg = 'OK'

        # Wait until time matches
        # Call to TEAM Engine to run test

        self.set_result(result, msg)


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

        result = True;
        msg = "OK"       
        if reliability < min_rel :
            result = False
            msg = "Service did not meet minimum SLA uptime requirement"
      
        self.set_result(result, msg)


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