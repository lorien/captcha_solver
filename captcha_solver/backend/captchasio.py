from .antigate import AntigateBackend

SOFTWARE_ID = 2373


class CaptchasIOBackend(AntigateBackend):
    def setup(self, api_key, service_url='https://api.captchas.io', **kwargs):
        super(CaptchasIOBackend, self).setup(api_key, service_url, **kwargs)

    def get_submit_captcha_request_data(self, data, **kwargs):
        # res is {url: ..., post_data: ...}
        res = super(CaptchasIOBackend, self).get_submit_captcha_request_data(
            data, **kwargs
        )
        res['post_data']['soft_id'] = SOFTWARE_ID
        return res		
