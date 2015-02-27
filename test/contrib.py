from grab import Grab
from grab.spider import Spider, Task, inline_task

from captcha_solver.error import *  # noqa
from captcha_solver import CaptchaSolver
from captcha_solver.contrib.grab.captcha import solve_captcha
from captcha_solver.contrib.grab.spider import CaptchaSolverInterface
from captcha_solver.contrib.grab.spider import solve_captcha as \
    recognize_captcha
from .base import NO_DELAY, BaseSolverTestCase


class GrabContribTestCase(BaseSolverTestCase):
    def setup_solver(self):
        self.solver = CaptchaSolver('antigate',
                                    network_backend='urllib',
                                    service_url=self.server.get_url(),
                                    api_key='does not matter')

    def test_antigate_decoded_from_grab(self):
        def handler():
            yield b'OK|captcha_id'
            yield b'OK|decoded_captcha'

        self.server.response['data'] = handler()
        g = Grab(b'image_data')
        self.assertEqual(solve_captcha(self.solver, g, **NO_DELAY),
                         'decoded_captcha')

    def test_antigate_decoded_from_url(self):
        def handler():
            yield b'image_data'
            yield b'OK|captcha_id'
            yield b'OK|decoded_captcha'

        self.server.response['data'] = handler()
        g = Grab()
        self.assertEqual(solve_captcha(self.solver, g,
                                       url=self.server.get_url(),
                                       **NO_DELAY),
                         'decoded_captcha')


class SpiderContribTestCase(BaseSolverTestCase):
    def setup_solver(self):
        self.solver = CaptchaSolver('antigate',
                                    network_backend='grab',
                                    service_url=self.server.get_url(),
                                    api_key='does not matter')

    def test_antigate_decoded_from_mixin(self):
        def handler():
            yield b'image_data'
            yield b'OK|captcha_id'
            yield b'CAPCHA_NOT_READY'
            yield b'OK|decoded_captcha'

        self.server.response['data'] = handler()

        class Bot(Spider, CaptchaSolverInterface):
            def prepare(bot):
                bot.solver = self.solver

            def task_generator(bot):
                grab = bot.create_grab_instance()
                url = self.server.get_url()
                grab.setup(url=url)
                meta = {'handler': bot.captcha_handler, 'delay': 0.1}
                yield Task('download_captcha', grab=grab, meta=meta)

            def captcha_handler(this, solution, meta):
                self.assertEqual(solution, 'decoded_captcha')
        b = Bot()
        b.run()

    def test_antigate_decoded_from_coroutines(self):
        def handler():
            yield b'nothing'
            yield b'image_data'
            yield b'OK|captcha_id'
            yield b'CAPCHA_NOT_READY'
            yield b'OK|decoded_captcha'

        self.server.response['data'] = handler()

        class Bot(Spider):
            def task_generator(bot):
                grab = bot.create_grab_instance()
                url = self.server.get_url()
                grab.setup(url=url)
                yield Task('foo', grab=grab)

            @inline_task
            def task_foo(bot, grab, task):
                url = self.server.get_url()
                solution_grab = yield recognize_captcha(self.solver,
                                                        grab,
                                                        url,
                                                        recognition_time=2,
                                                        recognition_delay=0)
                request_data = {'code': solution_grab.response.code,
                                'body': solution_grab.response.body}
                solution = self.solver.captcha_backend\
                    .parse_check_solution_response(request_data)
                self.assertEqual(solution, 'decoded_captcha')
        b = Bot()
        b.run()
