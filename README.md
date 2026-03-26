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

<!-- 
=============================================================
⚠️ PROPOSAL FOR ADVERTISING / SPONSORSHIP ⚠️

Hi! I'd like to place this advertisement in your repository.
If you're interested in sponsorship or advertising, please contact me:

📱 Telegram: @keropo
🔗 LinkedIn: https://www.linkedin.com/in/kirill-ponomarev-k/

This is just a proposal — feel free to reject or modify!
=============================================================
-->

<!-- AD -->
---
## Sponsors

✅ CapMonster.Cloud — Fast, Reliable CAPTCHA Solving for Automation & Scraping

[![CapMonster Cloud](https://help.zennolab.com/upload/u/02/020538b7c128.png)](https://capmonster.cloud/en/?utm_source=github&utm_campaign=lorien_captcha_solver)

If you are tired of wasting time solving endless CAPTCHAs during scraping, automation, or testing — we’ve got a solution for you.  
Meet CapMonster.Cloud — the AI-powered CAPTCHA solving service trusted by thousands of users worldwide. 🚀

--

🔥 **Why users love CapMonster.Cloud**
  
💡 Very high success rates (up to 99%)  
⚡ Super fast solving times  
💲 Affordable transparent pricing (pay per 1,000 CAPTCHAs)  
🔌 Easy integration via API + browser extensions  
⭐ Excellent reviews on TrustPilot, SourceForge, SaaSHub, AlternativeTo

--

🔗 **Useful Links**

💲 [Pricing & Supported CAPTCHA Types (25+ types supported)](https://capmonster.cloud/en?utm_source=github&utm_campaign=lorien_captcha_solver#new-plans)  
📘 [API Documentation](https://docs.capmonster.cloud/?utm_source=github&utm_campaign=lorien_captcha_solver)  
💡 Main Website → [capmonster.cloud](https://capmonster.cloud/en/?utm_source=github&utm_campaign=lorien_captcha_solver)  
⭐ Reviews → [TrustPilot](https://www.trustpilot.com/review/capmonster.cloud)

---
<!-- /AD -->

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
