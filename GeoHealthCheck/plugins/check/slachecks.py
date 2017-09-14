from GeoHealthCheck.plugin import Plugin
from GeoHealthCheck.check import Check
try:
    from html import escape  # python 3.x
except ImportError:
    from cgi import escape  # python 2.x

#-# imported for this plugin #-#
from pyquery import PyQuery
import os
import urllib
import re

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
        # TODO: Wait until time matches -- Don't do now...
        bp()

        uname = self.probe._resource.owner_identifier
        owner = User.query.filter_by(username=uname).first()        

        # Register user if they have not already been registerd in Team Engine
        # try:
        #     api = TeamEngineAPI(self.get_param('TEAM Engine endpoint'))
        #     api.register(owner.username, owner.password)
        #     api.authenticate(owner.username, owner.password)


        #     # TODO: Run test here.....


        # except Exception as err:
        #     print err
        #     traceback.print_stack()

        # ##### For Testing (from file) #####
        # try :
        #     lines = [];
        #     file = open(os.path.dirname(__file__) + "/../../../../results.xml")
        #     for line in file:
        #         lines.append(line)

        #     text = ''.join(lines).rstrip()
        #     self.set_result(True, text)

        # except Exception as err: 
        #     print(err)
        #     self.set_result(False, err)
        ###################################


        ############ The Real deal ########
        # try:
        #     te_test_endpoint = self.get_param('TEAM Engine endpoint')
        #     te_test_name = self.get_param('Test to Run')
        #     te_test_params = re.match(".+\[(.+)\]", te_test_name).groups()[0]
        # 
        #     # Must URL encode '&' chars per TEAM Engine documentation : 
        #     #   http://opengeospatial.github.io/teamengine/users.html
        #     resource_endpoint = self.probe.response.url.replace('&','%26')
        # 
        # 
        #     url = ("%s/rest/suites/%s/run?wfs=%s" % (te_test_endpoint, te_test_params, resource_endpoint)).replace('//rest','/rest')
        #     cleanUrl = url.replace('https', 'http').replace('//rest','/rest')
        #     print cleanUrl
        #     # resp = requests.get(cleanUrl)
        #     # text = resp.text
        # 
        #     # If the test ran without issue
        #     if resp.status_code == requests.codes.ok:
        #         doc = PyQuery(text.encode())
        #         failed = int(doc.attr('failed'))
        # 
        #         # report a pass or a fail
        #         if failed > 0 :
        #             self.set_result(False, text)
        #         else :
        #             self.set_result(True, text)
        # 
        #     # Error happened running test
        #     else:
        #         print text
        #         self.set_result(False, text)
        # 
        # except Exception as err:
        #     print err
        #     traceback.print_stack()
        #     self.set_result(False, err)
        #     return
        ###################################



"""
Check for verifying the uptime of a service
"""
class SlaVerifyUptime(Check):

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

        # get record of uptime...
        # get average
        # see if its above the given average...
        # 
        self.set_result(result, msg)
