import os
from time import sleep
from typing import Any, Callable
import keyboard

from rich.console import Console

console = Console()

def get_current_dirs() -> list[str]:
    """
    Get all directories in the current directory
    """
    
    #       Append current Path
    #       |        Make Path look local with a './'
    #       |        |                 Get all files and directories in current directory
    #       |        |                 |               Only append 'x' if it is a directory
    #       |        |                 |               |
    return ["./"] + [("./"+x) for x in os.listdir() if os.path.isdir(x)]

def simple_user_select(choices: list[str], prompt: str = None, new_line: bool = True,render=None) -> int:
    """
    Displays the `choices` on the screen and
    returns the index of the selected item
    """

    if prompt:
        console.print(f"[bold magenta]=== {prompt} ===[/bold magenta]")

    for i, choice in enumerate(choices):
        console.print(f"[cyan]([b]{i + 1}[/b])[/cyan]: [white]{choice}[/white]")

    index: int = None
    while index is None or index > len(choices) - 1 or index < 0:
        try:
            index = int(console.input(f"Select (1-{len(choices)}): ")) - 1
        except ValueError:
            console.print("[red]please enter a valid number[/red]")
    if new_line: print()
    return index

def fancy_user_select(
    choices: list, 
    render: Callable[[Any, bool], str] = lambda choice, _: choice, 
    prompt: str = None
    ) -> int:
    """
    Select something in a fancy way
    
    Example:
    ```
    choice
    > choice
    choice
    choice
    ```
    """

    selected = 0
    
    # Inner function, because it isn't 
    # needed outside of here
    def print_state():
        """
        Print the current state of the selection
        """
        
        # Clear the terminal screen
        os.system("cls||clear")

        if prompt:
            console.print(f"[bold magenta]=== {prompt} ===[/bold magenta]")
        console.print("[grey23]use 'w' and 's' for selection[/grey23]", end="\n\n")

        for i, choice in enumerate(choices):
            if i == selected:
                console.print(f"[bold cyan]> {render(choice, True)}[/bold cyan]")
            else:
                console.print(f"[grey46]{render(choice, False)}[/grey46]")

    print_state()

    while True:
        sleep(.1)
        pressed_key = keyboard.read_key()

        if pressed_key == "w": 
            if selected > 0:
                selected -= 1
            else:
                selected = len(choices) - 1 
        elif pressed_key == "s":
            if selected < len(choices) - 1:
                selected += 1
            else:
                selected = 0
        elif pressed_key == "enter":
            # Because the user pressed enter, input must be called to
            # remove that 'press'. Otherwise, after the cli finished,
            # the user would execute all the text he wrote while being in the cli
            input()
            print_state()
            return selected
        
        print_state()
