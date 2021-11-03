import sys
import argparse
from textgen import *


def cli_main():
    try:
        cliargs()
        cligui()
    except KeyboardInterrupt:
        # quit
        sys.exit(-1)


def cligui():
    print('Welcome to paper-cli please chose one of the following projects by there corresponding number')
    project_list()
    project = input('Your Input: ')
    print('Next Please select your Target Minecraft Version')
    version_group_list(int(project))
    mcversion = input('Your Input: ')
    build_list(int(project), int(mcversion))


def cliargs():
    praser = argparse.ArgumentParser(description='Arguments')
    praser.add_argument("--projects", "-p", type=float,
                        help="select the paper project ['paper', 'travertine', 'waterfall']")
    args = praser.parse_args()

