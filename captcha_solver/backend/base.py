from captcha_solver.const import TRANSPORT_BACKEND_ALIAS
from grab.util.module import import_string


class CaptchaBackend(object):
    def setup(self, transport='grab', **kwargs):
        if transport in TRANSPORT_BACKEND_ALIAS:
            backend_path = TRANSPORT_BACKEND_ALIAS[transport]
        else:
            backend_path = transport
        self.Transport = import_string(backend_path)
