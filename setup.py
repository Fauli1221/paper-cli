from setuptools import setup

setup(
    name='paper-cli',
    version='0.1.1',
    packages=['papercli'],
    install_requires=[
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'paper-cli = papercli.papercli:cli_main',
        ],
    },
)
