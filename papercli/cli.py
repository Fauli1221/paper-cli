"""import argparse sys urllib request and textgen and save"""
import argparse
import sys
from typing import Callable
import keyboard
import os

from papercli.paperapi import PaperApi, Build
from papercli.utility import *

api = PaperApi()

# CLI version
VERSION = "0.3.0"

def cli_main():
    """
    Main CLI method
    """

    project_ids = api.get_project_ids()

    parser = argparse.ArgumentParser(description='Arguments')
    parser.add_argument("--project", "-p", type=str, choices=project_ids,
                        help=f"select the paper project {project_ids}")
    parser.add_argument("--mcversion", "-mcv", type=str, help="Select target Minecraft Version")
    parser.add_argument("--build", "-b", type=int, help="Select Build")
    parser.add_argument("--destination", "-d", type=str,
                        help="Select the destination of the file")
    parser.add_argument("--latest", nargs='?', type=bool, const=True, help="Download latest version")
    parser.add_argument("--experimental", nargs='?', type=bool, const=True, default=False, help="Use the experimental cligui")
    parser.add_argument("--version", "-v", action="version", version=VERSION)
    args = parser.parse_args()

    destination = None
    if args.destination:
        destination = args.destination

    # Start interactive cli
    if args.project is None:
        cli_gui(destination, args.experimental)

    # Download build from flag information
    else:
        download_by_args(args, destination)


def cli_gui(destination: str = None, experimental: bool = False):
    """
    The interactive cli PaperMC downloader
    """
    select: Callable[[list], int] = fancy_user_select if experimental else simple_user_select

    console.print(
        "[bold yellow3]--- === welcome to the paper-cli! === ---[/bold yellow3]",
        f"[grey23]press {'any key' if experimental else 'enter'} to start the selection[/grey23]",
        sep="\n"
    )
    if experimental:
        keyboard.read_key()
    else:
        input()

    with console.status("", spinner="dots"):
        project_ids = api.get_project_ids()
    project = api.get_project(project_ids[
        select(project_ids, prompt="select a project")
        ])

    with console.status("", spinner="dots"):
        mc_version_groups = project.get_version_groups()
    mc_version_group = mc_version_groups[
        select(mc_version_groups, prompt="select your minecraft version group")
        ]

    with console.status("", spinner="dots"):
        # Get all versions that start with the 
        # selected version group in a list
        mc_versions = list(filter(
            lambda x: x.startswith(mc_version_group),
            project.get_versions()    
        ))
    mc_version = mc_versions[
        select(mc_versions, prompt="select your target minecraft version")
        ]

    with console.status("", spinner="dots"):
        builds = project.get_all_builds(mc_version)
    
    render = lambda choice, selected: choice.build if not selected else str(choice)
    build = builds[
        select(builds, render=render, prompt="select a build (lowest is latest)")
        ]

    if not destination:
        dirs = get_current_dirs()
        dest_dir = dirs[
            select(dirs, prompt="where do you want to install the file?")
        ]

        if not experimental:
            # Can't select a name using experimental mode,
            # Because input is blocked in some way
            name = console.input(
                    "[bold magenta]=== how should the file be called? ===[/bold magenta]\n[grey23]leave empty for default name[/grey23]\nName: "
                )
            if len(name) == 0:
                destination = dest_dir
            else:
                destination = os.path.join(dest_dir, name if name.endswith(".jar") else name + ".jar")
        else:
            destination = dest_dir

    if select(
        ["yes", "no"],
        prompt=f"Do you want to download {project.id}, build {build.build} for MC version {build.version} to {destination}?"
        ) == 0:
        with console.status("[bold green]downloading",spinner="aesthetic"):
            build.download(destination)
        console.print(
            f"[bold green]Successfully downloaded {project.id}, version {build.version} to {destination}[/bold green]"
        )
        sys.exit(0)
    else:
        console.print("[bold red]exiting...[/bold red]")
        sys.exit(0)

def download_by_args(args: list[str], destination: str):
    """
    Validate args & download build
    """
    build: Build

    if args.latest or not args.mcversion:
        build = api.latest_build()
    elif args.mcversion:
        if args.build:
            build = api.get_project(args.project).get_build(args.mcversion, args.build)
        else:
            build = api.get_project(args.project).get_latest_build(args.mcversion)

    with console.status("[bold green]downloading...", spinner="aesthetic"):
        build.download(destination)

    console.print(
        f"[bold green]Successfully downloaded build {build.build}, version {build.version} to {destination}[/bold green]"
    )


if __name__ == "__main__":
    cli_gui(None, True)