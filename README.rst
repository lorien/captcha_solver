==============
Captcha Solver
==============

.. image:: https://travis-ci.org/lorien/captcha_solver.png?branch=master
    :target: https://travis-ci.org/lorien/captcha_solver?branch=master

.. image:: https://coveralls.io/repos/lorien/captcha_solver/badge.svg?branch=master
    :target: https://coveralls.io/r/lorien/captcha_solver?branch=master


.. image:: https://img.shields.io/pypi/v/captcha-solver.svg
    :target: https://pypi.python.org/pypi/captcha-solver

.. image:: https://img.shields.io/pypi/l/captcha-solver.svg
    :target: https://pypi.python.org/pypi/captcha-solver


Univeral API to captcha solving services.


Browser Backend Example
=======================

.. code:: python

    from captcha_solver import CaptchaSolver

    solver = CaptchaSolver('browser')
    with open('captcha.png', 'rb') as inp:
        raw_data = inp.read()
    print(solver.solve_captcha(raw_data))


Antigate Backend Example
========================

.. code:: python

    from captcha_solver import CaptchaSolver

    your_antigate_key = '7244c9f21b3617b958d2c0e2a8a67e93'
    solver = CaptchaSolver('antigate', api_key=your_antigate_key)
    with open('captcha.png', 'rb') as inp:
        raw_data = inp.read()
    print(solver.solve_captcha(raw_data))


Installation
============

.. code:: bash

    pip install captcha-solver
