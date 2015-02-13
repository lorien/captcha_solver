==============
Captcha Solver
==============

.. image:: https://travis-ci.org/lorien/captcha-solver.png
    :target: https://travis-ci.org/lorien/captcha-solver

.. image:: https://coveralls.io/repos/lorien/captcha-solver/badge.svg
    :target: https://coveralls.io/r/lorien/captcha-solver


Univeral API to different captcha solving services.


Usage Example
=============

Example::

    from captcha_solver import CaptchaSolver
    solver = CaptchaSolver('browser')
    print(solver.solve_captcha(image))
