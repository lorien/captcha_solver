==============
Captcha Solver
==============

.. image:: https://travis-ci.org/lorien/captcha_solver.png?branch=master
    :target: https://travis-ci.org/lorien/captcha_solver?branch=master

.. image:: https://coveralls.io/repos/lorien/captcha_solver/badge.svg?branch=master
    :target: https://coveralls.io/r/lorien/captcha_solver?branch=master

.. image:: https://pypip.in/download/captcha-solver/badge.svg?period=month
    :target: https://pypi.python.org/pypi/captcha-solver

.. image:: https://pypip.in/version/captcha-solver/badge.svg
    :target: https://pypi.python.org/pypi/captcha-solver

.. image:: https://landscape.io/github/lorien/captcha_solver/master/landscape.png
   :target: https://landscape.io/github/lorien/captcha_solver/master

Univeral API to different captcha solving services.


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


Grab Example
============

.. code:: python

    from captcha_solver import CaptchaSolver
    from captcha_solver.contrib.grab.captcha import solve_captcha
    from grab import Grab


    g = Grab()
    solver = CaptchaSolver('browser')
    url = 'http://captcha.ru/captcha2/'
    print (solve_captcha(solver, g, url=url))


Installation
============

.. code:: bash

    pip install captcha_solver
