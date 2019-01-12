from .twocaptcha import TwocaptchaBackend


class RucaptchaBackend(TwocaptchaBackend):
    def setup(self, api_key, service_url='http://rucaptcha.com', **kwargs):
        super(RucaptchaBackend, self).setup(api_key, service_url, **kwargs)
