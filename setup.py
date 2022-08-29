from setuptools import setup

setup(
    name='paper-cli',
    version='0.2.3',
    packages=['papercli'],
    long_description='tool to easyly get paper',
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
