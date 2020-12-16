import typer
import string
import secrets
import pyperclip
from enum import Enum

app = typer.Typer(add_completion=False)


class Color(str, Enum):
    WHITE = "white"
    BRIGHT_CYAN = "cyan"
    BRIGHT_RED = "red"
    BRIGHT_YELLOW = "yellow"


def create_list(letters, numbers, symbols):
    char_list = []
    if letters:
        char_list += string.ascii_letters
    if numbers:
        char_list += string.digits
    if symbols:
        char_list += string.punctuation
    return char_list


def create_password(pwd_length: int, options: tuple) -> str:
    letter, number, symbol = options
    char_list = create_list(letter, number, symbol)
    pwd = "".join(secrets.choice(char_list) for _ in range(pwd_length))
    return pwd


@app.command(context_settings={"help_option_names": ["-h", "--help"]})
def main(
    pwd_length: int = typer.Argument(
        12,
        metavar="password length",
        help="Length of password, minimum is 8",
        min=8,
    ),
    letters: bool = typer.Option(
        True, "--letters", "-l", help="Do not include letters"
    ),
    numbers: bool = typer.Option(
        False, "--numbers", "-n", help="Include digits"
    ),
    symbols: bool = typer.Option(
        False, "--symbols", "-s", help="Include symbols"
    ),
    copy: bool = typer.Option(
        False, "--copy", "-c", help="Copy password to clipboard"
    ),
    fg_color: Color = typer.Option(
        Color.WHITE, "--fg-color", "-f", case_sensitive=False
    ),
):
    """
    Password generator
    """

    options = (letters, numbers, symbols)
    pwd = create_password(pwd_length, options)
    typer.secho(pwd, fg=fg_color)

    if copy:
        pyperclip.copy(pwd)
        typer.echo("Password has been copied to clipboard.")


if __name__ == "__main__":
    app()

