from .antigate import AntigateBackend

class CaptchaSolutionsBackend(AntigateBackend):
    def setup(self, api_key, service_url='https://www.captchasolutions.com/', **kwargs):
        super(CaptchaSolutionsBackend, self).setup(api_key, service_url, **kwargs)					 					