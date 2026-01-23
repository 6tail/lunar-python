from setuptools import setup
import sys

# 基础依赖
install_requires = []

# Python < 3.9 需要 tzdata 和 backports.zoneinfo 来支持时区
# Python >= 3.9 内置 zoneinfo，但仍可能需要 tzdata（取决于系统）
extras_require = {
    'tz': [
        'tzdata>=2020.1',  # IANA 时区数据库
    ],
    'tz-backport': [
        'backports.zoneinfo>=0.2.1;python_version<"3.9"',
        'tzdata>=2020.1',
    ],
}

setup(
    name='lunar_python',
    version='1.5.0',
    packages=['lunar_python', 'lunar_python.util', 'lunar_python.eightchar'],
    url='https://github.com/6tail/lunar-python',
    license='MIT',
    author='6tail',
    author_email='6tail@6tail.cn',
    description='lunar is a calendar library for Solar and Chinese Lunar with timezone/DST support.',
    long_description='''lunar is a calendar library for Solar and Chinese Lunar.

Features:
- Solar (Gregorian) and Lunar (Chinese) calendar conversion
- Eight Characters (八字) calculation
- 24 Solar Terms (节气)
- Chinese holidays and festivals
- Timezone and Daylight Saving Time (DST) support
  - Default timezone: Asia/Shanghai (includes China DST history 1986-1991)
  - Supports all IANA timezones for worldwide use
''',
    keywords='solar lunar chinese calendar timezone dst bazi',
    python_requires='>=3.6',
    install_requires=install_requires,
    extras_require=extras_require,
)
