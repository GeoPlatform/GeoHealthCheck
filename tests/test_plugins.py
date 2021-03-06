# =================================================================
#
# Authors: Tom Kralidis <tomkralidis@gmail.com>,
# Just van den Broecke <justb4@gmail.com>
#
# Copyright (c) 2014 Tom Kralidis
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

import unittest
import sys
import os
from GeoHealthCheck.models import DB, load_data
from GeoHealthCheck.views import get_probes_avail
from GeoHealthCheck.plugin import Plugin
from GeoHealthCheck.factory import Factory

TEST_DIR = os.path.dirname(os.path.abspath(__file__))

# Needed to find classes and plugins
sys.path.append('%s/..' % TEST_DIR)


class GeoHealthCheckTest(unittest.TestCase):
    def setUp(self):
        self.db = DB
        # do once per test
        load_data('%s/data/minimal.json' % TEST_DIR)

    def tearDown(self):
        self.db = DB
        # Needed for Postgres, otherwise hangs by aggressive locking
        self.db.session.close()
        self.db.drop_all()
        self.db.session.commit()
        self.db.session.close()

    def testPluginsPresent(self):

        plugins = Plugin.get_plugins('GeoHealthCheck.probe.Probe')
        for plugin in plugins:
            plugin = Factory.create_obj(plugin)
            self.assertIsNotNone(plugin)

            # Must have run_request method
            self.assertIsNotNone(plugin.run_request)

        plugins = Plugin.get_plugins('GeoHealthCheck.check.Check')
        for plugin in plugins:
            plugin = Factory.create_obj(plugin)
            self.assertIsNotNone(plugin)
            # Must have perform method
            self.assertIsNotNone(plugin.perform)

        plugins = Plugin.get_plugins(
            'GeoHealthCheck.probe.Probe',
            filters=[('RESOURCE_TYPE', 'OGC:*'), ('RESOURCE_TYPE', 'OGC:WMS')])

        for plugin in plugins:
            plugin_class = Factory.create_class(plugin)
            self.assertIsNotNone(plugin_class)

            plugin_obj = Factory.create_obj(plugin)
            self.assertIsNotNone(
                plugin_obj, 'Cannot create Plugin from string %s' + plugin)

            parameters = plugin_obj.PARAM_DEFS
            self.assertTrue(
                type(parameters) is dict, 'Plugin Parameters not a dict')

            checks = plugin_obj.CHECKS_AVAIL
            self.assertTrue(
                type(checks) is dict, 'Plugin checks not a dict')

            # Must have run_request method
            self.assertIsNotNone(plugin_obj.run_request)

            # Must have class var RESOURCE_TYPE='OGC:WMS'
            class_vars = Factory.get_class_vars(plugin)
            self.assertIn(class_vars['RESOURCE_TYPE'], ['OGC:WMS', 'OGC:*'])

    def testPluginParamDefs(self):
        plugin_obj = Factory.create_obj(
            'GeoHealthCheck.plugins.probe.owsgetcaps.WmsGetCaps')
        self.assertIsNotNone(plugin_obj)

        checks = plugin_obj.CHECKS_AVAIL
        self.assertEquals(len(checks), 3, 'WmsGetCaps should have 3 Checks')

        parameters = plugin_obj.PARAM_DEFS
        self.assertEquals(
            len(parameters), 2, 'WmsGetCaps should have 2 Parameters')

        probe_obj = Factory.create_obj(
            'GeoHealthCheck.plugins.probe.http.HttpGet')
        self.assertIsNotNone(probe_obj)
        check_vars = probe_obj.expand_check_vars(probe_obj.CHECKS_AVAIL)
        self.assertIsNotNone(check_vars)
        plugin_vars = probe_obj.get_plugin_vars()
        self.assertIsNotNone(plugin_vars)

    def testPluginChecks(self):
        plugin_obj = Factory.create_obj(
            'GeoHealthCheck.plugins.check.checks.NotContainsStrings')
        self.assertIsNotNone(plugin_obj)

        plugin_obj = Factory.create_obj(
            'GeoHealthCheck.plugins.check.checks.ContainsStrings')
        self.assertIsNotNone(plugin_obj)

        plugin_vars = plugin_obj.get_plugin_vars()
        self.assertIsNotNone(plugin_vars)

        parameters = plugin_obj.PARAM_DEFS
        self.assertEquals(
            len(parameters), 1, 'PARAM_DEFS should have 1 Parameter')
        self.assertEquals(parameters['strings']['type'], 'stringlist',
                          'PARAM_DEFS.strings[type] should be stringlist')

        plugin_obj = Factory.create_obj(
            'GeoHealthCheck.plugins.check.checks.NotContainsOwsException')
        self.assertIsNotNone(plugin_obj)

        parameters = plugin_obj.PARAM_DEFS
        self.assertEquals(
            len(parameters), 1, 'PARAM_DEFS should have 1 Parameter')
        self.assertEquals(
            parameters['strings']['value'][0], 'ExceptionReport>',
            'PARAM_DEFS.strings[0] should be ExceptionReport>')

    def testProbeViews(self):
        probes = get_probes_avail('OGC:WMS')
        self.assertIsNotNone(probes)


if __name__ == '__main__':
    unittest.main()
