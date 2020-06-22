from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name='lunar_python',
    version='1.0.4',
    packages=['lunar_python', 'lunar_python.util'],
    url='https://github.com/6tail/lunar-python',
    license='MIT',
    author='6tail',
    author_email='6tail@6tail.cn',
    description='lunar is a calendar library for Solar and Chinese Lunar.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='solar lunar'
)
