import logging

from grab.spider.task import Task
from captcha_solver.error import SolutionNotReady, CaptchaServiceError

logger = logging.getLogger('grab.spider.captcha')


def response_to_dict(grab):
    return {'code': grab.response.code,
            'body': grab.response.body}


class CaptchaSolverInterface(object):
    """
    Spider mixin for recognizing captcha that can be used in this way:
    class Bot(Spider, CaptchaSolverInterface):
        def prepare(self):
            self.solver = CaptchaSolver('antigate', 'grab', api_key='some api key')

        def task_generator(self):
            grab = self.create_grab_instance()
            url = 'http://captcha.ru/'
            grab.setup(url=url)
            yield Task('foo', grab=grab)

        def task_foo(self, grab, task):
            url = 'http://captcha.ru/captcha2/'
            grab.setup(url=url)
            meta = {'handler': self.captcha_handler, grab=grab}
            yield Task('download_captcha', grab=grab, meta=meta)

        def captcha_handler(self, solution, meta):
            print solution
            # return Task('another_foo', grab=meta['foo'])
    b = Bot()
    b.run()
    """
    def task_download_captcha(self, grab, task):
        logger.debug('Got captcha image')
        data = self.solver.captcha_backend.get_submit_captcha_request_data(grab.response.body)
        g_new = self.solver.network_backend.make_grab_instance(**data)
        yield Task('submit_captcha', grab=g_new, meta=task.meta)

    def task_submit_captcha(self, grab, task):
        captcha_id = self.solver.captcha_backend.parse_submit_captcha_response(response_to_dict(grab))
        data = self.solver.captcha_backend.get_check_solution_request_data(captcha_id)
        g_new = self.solver.network_backend.make_grab_instance(**data)
        yield Task('check_solution', grab=g_new, delay=5, meta=task.meta)

    def task_check_solution(self, grab, task):
        try:
            solution = self.solver.captcha_backend.parse_check_solution_response(response_to_dict(grab))
        except SolutionNotReady:
            logger.debug('Solution is not ready')
            yield task.clone(delay=task.original_delay)
        else:
            logger.debug('Got captcha solution: %s' % solution)
            yield task.meta['handler'](solution, task.meta)


def solve_captcha(solver, grab, url=None, delay=5, recognition_time=120, **kwargs):
    """
    :param solver: CaptchaService object
    :param grab: grab object with captcha image in body
    :return: grab object with captcha solution

    The function is subroutine that must be used in the inline task:

    class Bot(Spider):
        def task_generator(self):
            grab = self.create_grab_instance()
            url = 'http://captcha.ru/'
            grab.setup(url=url)
            yield Task('foo', grab=grab)

        @inline_task
        def task_foo(self, grab, task):
            solver = CaptchaSolver('antigate', 'grab', api_key='some api key')
            captcha_grab = grab.clone()
            url = 'http://captcha.ru/captcha2/'
            captcha_grab.setup(url=url)
            captcha_grab = yield Task(grab=captcha_grab)
            solution_grab = yield solve_captcha(solver, captcha_grab)
            solution = solver.captcha_backend.parse_check_solution_response({'code': solution_grab.response.code,
                                                                            'body': solution_grab.response.body})
    b = Bot()
    b.run()
    """
    if url:
        grab = grab.clone()
        grab.setup(url=url)
        grab = yield Task(grab=grab)
    logger.debug('Got captcha image')
    data = solver.captcha_backend.get_submit_captcha_request_data(grab.response.body, **kwargs)
    antigate_grab = solver.network_backend.make_grab_instance(**data)
    antigate_grab = yield Task(grab=antigate_grab)

    captcha_id = solver.captcha_backend.parse_submit_captcha_response(response_to_dict(antigate_grab))
    data = solver.captcha_backend.get_check_solution_request_data(captcha_id)
    antigate_grab = solver.network_backend.make_grab_instance(**data)

    for _ in xrange(0, recognition_time/delay, delay):
        antigate_grab = yield Task(grab=antigate_grab, delay=delay)
        try:
            solver.captcha_backend.parse_check_solution_response(response_to_dict(antigate_grab))
        except SolutionNotReady:
            logger.debug('Solution is not ready')
        else:
            return