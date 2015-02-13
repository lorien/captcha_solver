import importlib

from captcha_solver.const import TRANSPORT_BACKEND_ALIAS


class CaptchaBackend(object):
    def setup(self, transport='grab', **kwargs):
        if transport in TRANSPORT_BACKEND_ALIAS:
            backend_path = TRANSPORT_BACKEND_ALIAS[transport]
        else:
            backend_path = transport
        module_path, cls_name = backend_path.rsplit('.', 1)
        self.Transport = getattr(importlib.import_module(module_path), cls_name)
