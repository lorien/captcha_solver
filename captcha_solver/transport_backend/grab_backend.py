from grab import Grab


class GrabBackend(object):
    def request(self, url, data):
        g = Grab()
        if data:
            g.setup(post=data)
        g.go(url)
        return g.response

    def make_grab_instance(self, url, data):
        g = Grab()
        g.setup(url=url)
        if data:
            g.setup(post=data)
        return g