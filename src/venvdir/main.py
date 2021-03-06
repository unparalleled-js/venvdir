import click

from venvdir.error import _ErrorHandlingGroup
from venvdir.venvs import add_entry
from venvdir.venvs import get_entries
from venvdir.venvs import create_entry
from venvdir.venvs import get_entry
from venvdir.venvs import remove_entry
from venvdir.util import format_to_table
from venvdir.util import find_format_width

_CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
    "max_content_width": 200,
}


@click.command(name="ls")
def list_command():
    """Lists all managed virtual environments."""
    entries = get_entries()
    if not entries:
        return
    rows, column_size = find_format_width(entries)
    table = format_to_table(rows, column_size)
    click.echo(table)


name_arg = click.argument("Name")


def _create_path_option(required):
    return click.option(
        "--path",
        "-p",
        help="The path where to create the virtual environment. Uses ~/.venvdir/venvs/ if not given.",
        required=required,
    )


@click.command()
@name_arg
@_create_path_option(False)
def create(name, path):
    """Creates a new virtual environment."""
    create_entry(name, path)


@click.command()
@name_arg
@_create_path_option(True)
def add(name, path):
    """Adds an existing environment."""
    add_entry(name, path)


@click.command(name="rm")
@name_arg
def remove(name):
    """Removes and deletes a virtual environments and all its files."""
    remove_entry(name)


@click.command()
@name_arg
def which(name):
    """Shows the path to the virtual environment."""
    entry = get_entry(name)
    click.echo(entry.path)


HELP = """\b
    Activate a virtual environment by doing:
    \n\tsource venvdira <env-name>
"""


@click.group(cls=_ErrorHandlingGroup, context_settings=_CONTEXT_SETTINGS, help=HELP)
def cli():
    pass


cli.add_command(list_command)
cli.add_command(create)
cli.add_command(add)
cli.add_command(which)
cli.add_command(remove)
