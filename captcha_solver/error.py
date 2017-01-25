__all__ = ('CaptchaSolverError', 'CaptchaServiceError', 'SolutionNotReady',
           'ServiceTooBusy', 'BalanceTooLow', 'SolutionTimeoutError',
           'InvalidServiceBackend')


class CaptchaSolverError(Exception):
    pass


class CaptchaServiceError(CaptchaSolverError):
    pass


class SolutionNotReady(CaptchaServiceError):
    pass


class SolutionTimeoutError(SolutionNotReady):
    pass


class ServiceTooBusy(CaptchaServiceError):
    pass


class BalanceTooLow(CaptchaServiceError):
    pass


class InvalidServiceBackend(CaptchaSolverError):
    pass
