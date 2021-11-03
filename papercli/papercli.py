import sys
import argparse
from textgen import *
import urllib.request
from save import selected_builds, selected_mc_version, projects_list, build_name


def cli_main():
    try:
        cliargs()
        cligui()
    except KeyboardInterrupt:
        # quit
        sys.exit(-1)


def downloade(build, version, p_project, filename):
    url = f'https://papermc.io/api/v2/projects/{p_project}/versions/{version}/builds/{build}/downloads/{filename}'
    urllib.request.urlretrieve(url, fr'./{p_project}.jar')


def cligui():
    print('Welcome to paper-cli please chose one of the following projects by there corresponding number')
    project_list()
    project = input('Your Input: ')
    print('Next Please select your Target Minecraft Version')
    version_group_list(int(project))
    mcversion = input('Your Input: ')
    build_list(int(project), int(mcversion))
    build_input = input('Your Input: ')
    build = selected_builds[int(build_input)*2+1]
    version = selected_mc_version[int(build_input)*2+1]
    p_project = projects_list[int(project)]
    filename = build_name[int(build_input)*2+1]
    print('Do you want to Downloade {projectname} build {build} for MC version {mcversion}?'.format(projectname=p_project, build=build, mcversion=version))
    downloade_question = input('(y/n): ').lower()
    if downloade_question == "y":
        downloade(build, version, p_project, filename)
        print('Downloadet')
    elif downloade_question == "n":
        print('exiting')
        sys.exit(0)
    else:
        print('error invalid anser exeting')
        sys.exit(1)


def cliargs():
    praser = argparse.ArgumentParser(description='Arguments')
    praser.add_argument("--projects", "-p", type=float,
                        help="select the paper project ['paper', 'travertine', 'waterfall']")
    args = praser.parse_args()

