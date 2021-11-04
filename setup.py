from setuptools import setup

setup(
    name='paper-cli',
    version='0.1.4',
    packages=['papercli'],
    install_requires=[
        'requests',
        'rich'
    ],
    entry_points={
        'console_scripts': [
            'paper-cli = papercli.papercli:cli_main',
        ],
    },
)
