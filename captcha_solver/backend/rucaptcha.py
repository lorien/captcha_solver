from .antigate import AntigateBackend


class RucaptchaBackend(AntigateBackend):
    def setup(self, api_key, service_url='http://rucaptcha.com', **kwargs):
        super(RucaptchaBackend, self).setup(api_key, service_url, **kwargs)
