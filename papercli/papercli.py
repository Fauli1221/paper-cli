"""import argparse sys urllib request and textgen and save"""
import argparse
import sys
import urllib.request

from papercli.save import selected_builds, selected_mc_version, projects_list, build_name
from papercli.textgen import project_list, version_group_list, build_list


def cli_main():
    """Main"""
    try:
        cliargs()
    except KeyboardInterrupt:
        # quit
        sys.exit(-1)


def downloade(build, version, p_project, filename):
    """Downloade File"""
    url = f'https://papermc.io/api/v2/projects/{p_project}/versions/{version}/builds/{build}/downloads/{filename}'
    urllib.request.urlretrieve(url, fr'./{p_project}.jar')


def cligui():
    """Cli GUI"""
    print('Welcome to paper-cli please chose one of the following projects by there corresponding number')
    project_list()
    project = input('Your Input: ')
    print('Next Please select your Target Minecraft Version')
    version_group_list(int(project))
    mcversion = input('Your Input: ')
    build_list(int(project), int(mcversion))
    build_input = input('Your Input: ')
    build = selected_builds[int(build_input) * 2 + 1]
    version = selected_mc_version[int(build_input) * 2 + 1]
    p_project = projects_list[int(project)]
    filename = build_name[int(build_input) * 2 + 1]
    print(f'Do you want to Downloade {p_project} build {build} for MC version {version}?')
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
    praser.add_argument("--projects", "-p", type=str,
                        help="select the paper project ['paper', 'travertine', 'waterfall']")
    praser.add_argument("--latest", type=bool, help="Downloade latest version")
    args = praser.parse_args()
    switch = {
        "paper": arg_paper,
        "travertine": arg_travertine,
        "arg_waterfall": arg_waterfall
    }
    try:
        project_id = switch[args.projects]()
    except KeyError:
        cligui()


def arg_paper():
    return '0'


def arg_travertine():
    return '1'


def arg_waterfall():
    return '2'
