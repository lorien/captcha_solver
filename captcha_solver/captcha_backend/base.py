from captcha_solver.const import TRANSPORT_BACKEND_ALIAS
from grab.util.module import import_string


class CaptchaBackend(object):
    def setup(self, **kwargs):
        pass
