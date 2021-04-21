from dotpyle.services.config_checker import ConfigChecker


class ConfigCheckerDecorator:
    """"""

    def __init__(self, arg):
        self._arg = arg
        self.checker = ConfigChecker()

    def __call__(self, *args, **kwargs):
        instance = self._arg.__new__(self._arg)
        instance.checker = self.checker
        instance.__init__(*args, **kwargs)

        return instance