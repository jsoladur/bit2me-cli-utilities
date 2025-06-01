from typer import Typer
from bit2me_cli_utilities.infrastructure.services.global_summary_service import (
    GlobalSummaryService,
)
from rich import print as rprint

command_group_name = "global-summary"
command_group_description = "Bit2Me Global Summary"
command_group: Typer = Typer()

global_summary_service: GlobalSummaryService = GlobalSummaryService()


# see https://typer.tiangolo.com/tutorial/
# for adding options or arguments
@command_group.command(
    "show",
    help="Show the global summary of Bit2Me",
)
def show():
    global_summary = global_summary_service.get_global_summary()
    rprint("==========================")
    rprint("BIT2ME GLOBAL SUMMARY")
    rprint("==========================")
    rprint(f"TOTAL DEPOSIT: {global_summary.total_deposits:.2f} EUR")
    rprint(f"WITHDRAWALS: {global_summary.withdrawls:.2f} EUR")
    rprint(f"CURRENT: {global_summary.current_value:.2f} EUR")
    rprint("----------------")
    rprint(
        f"NET REVENUE: {((global_summary.current_value - global_summary.total_deposits) + global_summary.withdrawls):.2f} EUR"
    )
    rprint("==========================")


__all__ = [command_group_name, command_group_description, command_group]
