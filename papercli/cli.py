"""import argparse sys urllib request and textgen and save"""
import argparse
import sys
from rich.console import Console

from papercli.paperapi import PaperApi, Build

console = Console()
api: PaperApi = PaperApi()

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
    parser.add_argument("--version", "-v", action="version", version=VERSION)
    args = parser.parse_args()

    destination = None
    if args.destination:
        destination = args.destination

    # Start interactive cli
    if args.project is None:
        cligui(destination)

    # Download build from flag information
    else:
        arg_check(args, destination)


def cligui(destination: str):
    """
    The interactive cli PaperMC downloader
    """

    print("Welcome to paper-cli!")
    project_ids = api.get_project_ids()
    project = api.get_project(project_ids[user_select(project_ids, "select a project")])

    mc_versions = project.get_versions()
    mc_version = mc_versions[user_select(mc_versions, "select your target minecraft version")]

    builds = project.get_build_numbers(mc_version)
    build = project.get_build(mc_version, builds[user_select(builds, "select a build (lowest is latest)")])

    if destination is None:
        destination = "./"

    if user_select(
        ["yes", "no"],
        f"Do you want to download {project.id}, build {build.build} for MC version {build.version}?"
       ) == 0:
        with console.status("[bold green]downloading...", spinner="aesthetic"):
            build.download(destination)
        console.print(
            f"[bold green]Successfully downloaded {project.id}, version {build.version} to {destination}[/bold green]"
        )
        sys.exit(0)
    else:
        console.print("[bold red]exiting...[/bold red]")
        sys.exit(0)


def user_select(choices: list[str], prompt: str = None) -> int:
    """
    Displays the `choices` on the screen and
    returns the index of the selected item
    """
    if prompt is not None:
        console.print(f"[bold magenta]=== {prompt} ===[/bold magenta]")

    for i, choice in enumerate(choices):
        console.print(f"[cyan]([b]{i + 1}[/b])[/cyan]: {choice}")

    index = int(console.input(f"Select (1-{len(choices)}): ")) - 1
    return index


def arg_check(args: list[str], destination: str):
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
    cligui("./")
