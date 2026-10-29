from setuptools import setup, find_packages
import re
from pathlib import Path

# Read version from lunar_python/__init__.py
def get_version():
    init_file = Path(__file__).parent / 'lunar_python' / '__init__.py'
    content = init_file.read_text(encoding='utf-8')
    match = re.search(r"^__version__\s*=\s*['\"]([^'\"]+)['\"]", content, re.M)
    if match:
        return match.group(1)
    raise RuntimeError("Unable to find version string.")

# Read long description from README
def get_long_description():
    readme_file = Path(__file__).parent / 'README_EN.md'
    if readme_file.exists():
        return readme_file.read_text(encoding='utf-8')
    return 'lunar is a calendar library for Solar and Chinese Lunar.'

setup(
    name='lunar_python',
    version=get_version(),
    packages=find_packages(include=['lunar_python', 'lunar_python.*']),
    url='https://github.com/6tail/lunar-python',
    license='MIT',
    author='6tail',
    author_email='6tail@6tail.cn',
    description='lunar is a calendar library for Solar and Chinese Lunar.',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    keywords='solar lunar chinese calendar traditional bazi eight-char jieqi festival',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
    ],
    project_urls={
        'Documentation': 'https://6tail.cn/calendar/api.html',
        'Source': 'https://github.com/6tail/lunar-python',
        'Bug Tracker': 'https://github.com/6tail/lunar-python/issues',
        'Changelog': 'https://github.com/6tail/lunar-python/blob/master/CHANGELOG.md',
    },
)
