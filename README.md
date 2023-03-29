# Captcha Solver Documentation

[![Test Status](https://github.com/lorien/captcha_solver/actions/workflows/test.yml/badge.svg)](https://github.com/lorien/captcha_solver/actions/workflows/test.yml)
[![Code Quality](https://github.com/lorien/captcha_solver/actions/workflows/check.yml/badge.svg)](https://github.com/lorien/captcha_solver/actions/workflows/test.yml)
[![Type Check](https://github.com/lorien/captcha_solver/actions/workflows/mypy.yml/badge.svg)](https://github.com/lorien/captcha_solver/actions/workflows/mypy.yml)
[![Test Coverage Status](https://coveralls.io/repos/github/lorien/captcha_solver/badge.svg)](https://coveralls.io/github/lorien/captcha_solver)
[![Documentation Status](https://readthedocs.org/projects/captcha_solver/badge/?version=latest)](https://captcha_solver.readthedocs.org)

Univeral API to work with captcha solving services.

Feel free to give feedback in Telegram groups: [@grablab](https://t.me/grablab) and [@grablab\_ru](https://t.me/grablab_ru)

## Installation

Run: `pip install -U captcha-solver`

## Twocaptcha Backend Example

Service website is https://2captcha.com?from=3019071

```python
from captcha_solver import CaptchaSolver

solver = CaptchaSolver('twocaptcha', api_key='2captcha.com API HERE')
raw_data = open('captcha.png', 'rb').read()
print(solver.solve_captcha(raw_data))
```

## Rucaptcha Backend Example

Service website is https://rucaptcha.com?from=3019071

```python
from captcha_solver import CaptchaSolver

solver = CaptchaSolver('rucaptcha', api_key='RUCAPTCHA_KEY')
raw_data = open('captcha.png', 'rb').read()
print(solver.solve_captcha(raw_data))
```

## Browser Backend Example
```python
from captcha_solver import CaptchaSolver

solver = CaptchaSolver('browser')
raw_data = open('captcha.png', 'rb').read()
print(solver.solve_captcha(raw_data))
```

## Antigate Backend Example

Service website is http://getcaptchasolution.com/ijykrofoxz

```python
from captcha_solver import CaptchaSolver

solver = CaptchaSolver('antigate', api_key='ANTIGATE_KEY')
raw_data = open('captcha.png', 'rb').read()
print(solver.solve_captcha(raw_data))
```

## DeathByCaptcha Backend Example

Service website is http://getcaptchasolution.com/ijykrofoxz

```python
from captcha_solver import CaptchaSolver

solver = DeathByCaptchaSolver(username="username", password='password')
raw_data = open('captcha.png', 'rb').read()
print(solver.solve_captcha(raw_data))
```
