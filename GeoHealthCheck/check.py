from plugin import Plugin


class Check(Plugin):
    """
     Base class for specific implementations to perform a check
     on Result from a Probe.

    """

    TAGS = []

    # Check parameter definitions, defaults, subclassses override
    PARAM_DEFS = {}

    # Lifecycle
    def init(self, probe, parameters):
        """
        Initialize Checker with parent Probe and parameters dict.
        :return:
        """
        self.probe = probe
        self._parameters = parameters

    # Lifecycle
    def perform(self):
        """
        Perform the Checker's specific check.
        :return:
        """
        return True, 'OK'
