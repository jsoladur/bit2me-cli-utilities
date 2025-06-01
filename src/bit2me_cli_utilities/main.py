import typer
from bit2me_cli_utilities.cli.global_summary_cli import (
    command_group_name,
    command_group_description,
    command_group,
)

app = typer.Typer()
app.add_typer(
    command_group,
    name=command_group_name,
    help=command_group_description,
)


if __name__ == "__main__":
    app()
