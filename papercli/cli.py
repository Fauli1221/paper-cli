"""import argparse sys urllib request and textgen and save"""
import argparse
import sys
import urllib.request

from papercli.paperapi import PaperApi, Build
from colorama import Fore

api: PaperApi = PaperApi()

def cli_main():
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

def download(build, version, p_project, filename, your_filename):
    """Download File"""
    url = f'https://papermc.io/api/v2/projects/{p_project}/versions/{version}/builds/{build}/downloads/{filename}'
    print(f'Downloading {p_project} build {build} for MC Version {version}')
    print(f'File will be saved as {your_filename}')
    urllib.request.urlretrieve(url, fr'./{your_filename}')


def cligui(destination):
    """Cli GUI"""
    print("Welcome to paper-cli!")
    project_ids = api.get_project_ids()
    project = api.get_project(project_ids[user_select(project_ids, "select a project")])

    mc_versions = project.get_versions()
    mc_version = mc_versions[user_select(mc_versions, "select your target minecraft version")]

    builds = project.get_build_numbers(mc_version)
    build = project.get_build(mc_version, builds[user_select(builds, "select a build (lowest is latest)")])

    if destination is None:
        destination = "./"

    if user_select(["yes", "no"], f"Do you want to download {project.id}, build {build.build} for MC version {build.version}?") == 0:
        print(Fore.BLUE + "downloading...", Fore.RESET, end="\r")
        build.download(destination)
        print(Fore.GREEN + "download finished!")
        sys.exit(0)
    else:
        print("exiting")
        sys.exit(0)


def user_select(choices: list[str], prompt: str = None, end="\n") -> int:
    """
    Returns the index of the selected item
    """
    if prompt is not None:
        print(Fore.MAGENTA, "===", prompt, "===", Fore.RESET)

    for i, choice in enumerate(choices):
        print(f"{Fore.CYAN}({Fore.WHITE}{i + 1}{Fore.CYAN}){Fore.RESET}: {choice}")
    
    index = int(input(f"Select (1-{len(choices)}): {Fore.BLUE}")) - 1
    print(Fore.RESET, end)
    return index


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
    # print(user_select(api.get_project_ids()))
    cligui("./")