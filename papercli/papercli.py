"""import argparse sys urllib request and textgen and save"""
import argparse
import sys
import urllib.request

from papercli.api import projects, versions, builds, build_info
from papercli.save import selected_builds, selected_mc_version, projects_list, build_name, versions_list, builds_list
from papercli.textgen import project_list, version_group_list, build_list


def cli_main():
    """Main"""
    try:
        projects()
        cliargs()
    except KeyboardInterrupt:
        # quit
        sys.exit(-1)


def downloade(build, version, p_project, filename, your_filename):
    """Downloade File"""
    url = f'https://papermc.io/api/v2/projects/{p_project}/versions/{version}/builds/{build}/downloads/{filename}'
    print(f'Downloading {p_project} build {build} for MC Version {version}')
    print(f'File will be saved as {your_filename}')
    urllib.request.urlretrieve(url, fr'./{your_filename}')


def cligui(your_filename):
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
    if your_filename is None:
        your_filename = f'{p_project}.jar'
    downloade_question = input('(y/n): ').lower()
    if downloade_question == "y":
        downloade(build, version, p_project, filename, your_filename)
        print('Downloadet')
        sys.exit(0)
    elif downloade_question == "n":
        print('exiting')
        sys.exit(0)
    else:
        print('error invalid anser exeting')
        sys.exit(1)


def cliargs():
    """create cli args"""
    praser = argparse.ArgumentParser(description='Arguments')
    praser.add_argument("--projects", "-p", type=str, choices=projects_list,
                        help=f"select the paper project {projects_list}")
    praser.add_argument("--version", "-v", type=str, help="Select target Minecraft Version")
    praser.add_argument("--build", "-b", type=int, help="Select Build")
    praser.add_argument("--filename", "-f", type=str,
                        help="Select your filename when unset it defaults to {projectname}.jar")
    praser.add_argument("--latest", nargs='?', type=bool, const=True, help="Download latest version")
    args = praser.parse_args()
    your_filename = None
    if args.filename:
        your_filename = args.filename
    if args.projects is None:
        cligui(your_filename)
    else:
        arg_check(args, your_filename)


def arg_paper():
    """return paper id"""
    return 0


def arg_travertine():
    """return travertine id"""
    return 1


def arg_waterfall():
    """return waterfall id"""
    return 2


def fetch_latest(project_id, your_filename):
    """fetch latst build"""
    projects()
    versions(project_id)
    latest_version = len(versions_list) - 1
    builds(project_id, latest_version)
    latest_build = len(builds_list) - 1
    latest_build_info = build_info(project_id, latest_version, latest_build)
    filename = latest_build_info['downloads']['application']['name']
    downloade(builds_list[-1], versions_list[-1], projects_list[project_id], filename, your_filename)


def arg_check(args, your_filename):
    """argument logik"""
    try:
        switch = {
            "paper": arg_paper,
            "travertine": arg_travertine,
            "arg_waterfall": arg_waterfall
        }
        project_id = switch[args.projects]()
        if args.latest:
            fetch_latest(project_id, your_filename)
        elif args.version:
            version = args.version
            if args.build:
                build = args.build
            else:
                build = builds(project_id, versions(project_id).index(version))[-1]
        try:
            sel_version = versions(project_id).index(version)
        except ValueError:
            print("an error ocurred please check your input")
            sys.exit(3)
        try:
            latest_build_info = build_info(project_id, sel_version, build)
            filename = latest_build_info['downloads']['application']['name']
        except KeyError:
            print("an error ocurred please check your input")
            sys.exit(4)
        if your_filename is None:
            your_filename = str(projects_list[project_id]) + '.jar'
        downloade(build, version, projects_list[project_id], filename, your_filename)
    except KeyError:
        print("an error ocurred please check your input")
        sys.exit(1)
    except UnboundLocalError:
        print("an error ocurred please check your input")
        sys.exit(2)
