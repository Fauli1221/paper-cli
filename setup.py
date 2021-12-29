from setuptools import setup

setup(
    name='paper-cli',
    version="0.3.0",
    packages=['papercli'],
    install_requires=[
        'requests',
        'rich',
        'keyboard'
    ],
    entry_points={
        'console_scripts': [
            'paper-cli = papercli.cli:cli_main',
        ],
    },
)
