from unittest import TestCase
from test_server import TestServer

NO_DELAY = {'recognition_time': 1,
            'recognition_delay': 0,
            'submiting_time': 1,
            'submiting_delay': 0}


class BaseSolverTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = TestServer()
        cls.server.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def setUp(self):
        self.setup_solver()
        self.server.reset()

    def setup_solver(self):
        raise NotImplementedError
