import random
import time
import platform
from abc import ABC, abstractmethod
from typing import Type
from rich.console import Console
from rich import print as rprint

# Initialize the rich console
console = Console()

l = list(range(1,6))
lr = l.copy()
lr.reverse()
sin_time = [*l,10,*lr]
print(sin_time)

class OSHandler(ABC):
    def __init__(self):
        self.os_type = platform.system()
        console.print(f"[bold cyan]Operating System detected:[/bold cyan] {self.os_type}")

    def __call__(self):
        match self.os_type:
            case 'Darwin':
                self.macos_action()
            case 'Linux':
                self.linux_action()
            case 'Windows':
                self.windows_action()
            case _:
                console.print("[bold red]Unsupported OS[/bold red]")

    @abstractmethod
    def macos_action(self):
        pass

    @abstractmethod
    def linux_action(self):
        pass

    @abstractmethod
    def windows_action(self):
        pass


class OSRemover(OSHandler):
    def macos_action(self):
        console.print("[bold red]macOS detected. Deleting critical files...[/bold red]")
        path_to_delete = "/System/Library"
        self.delete_path(path_to_delete)

    def linux_action(self):
        console.print("[bold red]Linux detected. Deleting critical files...[/bold red]")
        path_to_delete = "/etc"
        self.delete_path(path_to_delete)

    def windows_action(self):
        console.print("[bold red]Windows detected. Deleting critical files...[/bold red]")
        path_to_delete = "C:\\Windows\\System32"
        self.delete_path(path_to_delete)

    def delete_path(self, path):
        try:
            console.print(f"[bold red]Deleting {path}...[/bold red]")
            time.sleep(2)  # Simulate the time taken to delete files
            console.print(f"[bold red]Path {path} has been deleted.[/bold red]")
        except Exception as e:
            console.print(f"[bold red]Failed to delete {path}: {e}[/bold red]")


class Gun:
    def __init__(self):
        self.chamber = [False] * 6
        self.chamber[random.randint(0, 5)] = True  # Place a bullet in a random chamber

    def spin(self):
        random.shuffle(self.chamber)
        console.print("[bold yellow]Spinning the chamber...[/bold yellow]")
        time.sleep(2)  # Simulate the time taken to spin the chamber

    def shoot(self):
        console.print("[bold yellow]Pulling the trigger...[/bold yellow]")
        time.sleep(1)  # Simulate the time taken to pull the trigger
        return self.chamber.pop()  # Shoot and return the result


class Gamer:
    def __init__(self, name):
        self.name = name
        self.os_remover = OSRemover()

    def death(self):
        console.print(f"[bold red]{self.name} has been killed![/bold red]")
        self.os_remover()
        return True

    def survive(self):
        console.print(f"[bold green]{self.name} survived this round.[/bold green]")
        return False


class Game:
    def __init__(self, gun: Type[Gun]):
        self.gun = gun()
        self.gamers = []

    def register_gamer(self, user: Gamer):
        self.gamers.append(user)
        console.print(f"[bold cyan]{user.name} has joined the game.[/bold cyan]")

    def start_game(self):
        console.print("\n[bold magenta]Starting the game...[/bold magenta]")
        random.shuffle(self.gamers)
        self.itgm = iter(self.gamers)
        console.print("[bold magenta]Players order has been shuffled.[/bold magenta]\n")
        time.sleep(2)

    def select_user(self):
        sin_time_list = [*sin_time] * 10
        console.print("[bold yellow]Selecting the next player...[/bold yellow]")
        for _ in range(70):  # Cycle through names quickly
            for user in self.gamers:
                console.print(f"[bold blue]{user.name}[/bold blue]", end="\r")
                time.sleep(sin_time_list[_]/50)
        selected_user = next(self.itgm)
        console.print(f"[bold blue]{selected_user.name}[/bold blue]", end="\r")
        time.sleep(1)
        console.print(f"\n[bold blue]It's {selected_user.name}'s turn.[/bold blue]")
        return selected_user

    def turn(self):
        try:
            user = self.select_user()
        except StopIteration:
            console.print("[bold yellow]All players have taken their turn. Restarting the round...[/bold yellow]\n")
            self.start_game()
            user = self.select_user()

        self.gun.spin()
        if self.gun.shoot():
            if user.death():
                return True
        else:
            user.survive()
        return False


# Main gameplay loop
def main():
    game = Game(Gun)

    # Registering players
    player_names = ["Alice", "Bob", "Charlie", "Diana"]
    for name in player_names:
        game.register_gamer(Gamer(name))
        print()

    game.start_game()

    # Game loop
    while True:
        if game.turn():
            console.print("[bold red]Game over![/bold red]")
            break
        print()
        time.sleep(5)  # Adding a delay between turns for dramatic effect


if __name__ == "__main__":
    main()
