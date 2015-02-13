==============
Captcha Solver
==============

.. image:: https://travis-ci.org/lorien/captcha_solver.svg?branch=master
    :target: https://travis-ci.org/lorien/captcha_solver

.. image:: https://coveralls.io/repos/lorien/captcha_solver/badge.svg
    :target: https://coveralls.io/r/lorien/captcha_solver


Univeral API to different captcha solving services.


Usage Example
=============

Example::

    from captcha_solver import CaptchaSolver
    solver = CaptchaSolver('browser')
    print(solver.solve_captcha(image))
