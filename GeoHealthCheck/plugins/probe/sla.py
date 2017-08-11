import random
import traceback

from GeoHealthCheck.probe import Probe
from GeoHealthCheck.result import Result
from owslib.wms import WebMapService


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
        'GeoHealthCheck.plugins.check.slachecks.SlaPreformant': {
            'default': True
        }
    }
    """
    Checks avail for all specific Caps checks.
    Optionally override Check PARAM_DEFS using set_params
    e.g. with specific `value`.
    """

    def __init__(self):
        Probe.__init__(self)

    # def perform_request(self):
    #     """
    #     Perform the SLA check.
    #     See https://github.com/geopython/OWSLib/blob/
    #     master/tests/doctests/wms_GeoServerCapabilities.txt
    #     """


    #     # Add to overall Probe result
    #     self.result.add_result(True)
