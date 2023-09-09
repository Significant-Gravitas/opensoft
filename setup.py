from setuptools import setup

setup(
    name="run",
    version='0.1',
    py_modules=['run'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        run=run:run
    ''',
)
