"""import argparse sys urllib request and textgen and save"""
import argparse
import sys
import urllib.request

from api import PaperApi, Build
from papercli.save import selected_builds, selected_mc_version, projects_list, build_name, versions_list, builds_list
from papercli.textgen import project_list, version_group_list, build_list

from colorama import Fore

api: PaperApi = PaperApi()

def cli_main():
    """Main"""
    try:
        cliargs()
    except KeyboardInterrupt:
        # quit
        sys.exit(-1)


def download(build, version, p_project, filename, your_filename):
    """Download File"""
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
    print(f'Do you want to Download {p_project} build {build} for MC version {version}?')
    if your_filename is None:
        your_filename = f'{p_project}.jar'
    download_question = input('(y/n): ').lower()
    if download_question == "y":
        download(build, version, p_project, filename, your_filename)
        print('Downloadt')
        sys.exit(0)
    elif download_question == "n":
        print('exiting')
        sys.exit(0)
    else:
        print('error invalid anser exeting')
        sys.exit(1)


def cliargs():
    """create cli args"""
    project_ids = api.get_project_ids()

    praser = argparse.ArgumentParser(description='Arguments')
    praser.add_argument("--project", "-p", type=str, choices=project_ids,
                        help=f"select the paper project {project_ids}")
    praser.add_argument("--version", "-v", type=str, help="Select target Minecraft Version")
    praser.add_argument("--build", "-b", type=int, help="Select Build")
    praser.add_argument("--destination", "-d", type=str,
                        help="Select the destination of the file")
    praser.add_argument("--latest", nargs='?', type=bool, const=True, help="Download latest version")
    args = praser.parse_args()
    
    destination = None
    if args.destination:
        destination = args.destination

    # Start interactive cli
    if args.project is None:
        cligui(destination)

    # Download build from flag information
    else:
        arg_check(args, destination)

def arg_check(args: list[str], destination: str):
    """argument logik"""
    build: Build
    destination: str

    if args.latest or not args.version:
        build = api.latest_build()
    elif args.version:
        if args.build:
            build = api.get_project(args.project).get_build(args.version, args.build)
        else:
            build = api.get_project(args.project).get_latest_build(args.version)
    
    build.download(destination)


if __name__ == "__main__":
    pass