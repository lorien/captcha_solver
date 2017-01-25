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


Installation
============

.. code:: bash

    pip install captcha-solver


Browser Backend Example
=======================

.. code:: python

    from captcha_solver import CaptchaSolver

    solver = CaptchaSolver('browser')
    raw_data = open('captcha.png', 'rb').read()
    print(solver.solve_captcha(raw_data))


Antigate Backend Example
========================

.. code:: python

    from captcha_solver import CaptchaSolver

    solver = CaptchaSolver('antigate', api_key='ANTIGATE_KEY')
    raw_data = open('captcha.png', 'rb').read()
    print(solver.solve_captcha(raw_data))


Rucaptcha Backend Example
========================

.. code:: python

    from captcha_solver import CaptchaSolver

    solver = CaptchaSolver('rucaptcha', api_key='RUCAPTCHA_KEY')
    raw_data = open('captcha.png', 'rb').read()
    print(solver.solve_captcha(raw_data))
