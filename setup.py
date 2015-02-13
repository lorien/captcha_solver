from setuptools import setup, find_packages
import os

ROOT = os.path.dirname(os.path.realpath(__file__))
version = __import__('captcha_solver').__version__

setup(
    name = 'captcha-solver',
    version = version,
    description = 'Universal API to different captcha solving services',
    long_description = open(os.path.join(ROOT, 'README.rst')).read(),
    author = 'Gregory Petukhov',
    author_email = 'lorien@lorien.name',
    packages = find_packages(),
    license = "MIT",
    classifiers = (
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
)
