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


Usage Example
=============

.. code:: python

    from captcha_solver import CaptchaSolver
    solver = CaptchaSolver('browser')
    print(solver.solve_captcha(image))


Installation
============

.. code:: bash

    pip install captcha_solver
