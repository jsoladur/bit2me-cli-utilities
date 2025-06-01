import pandas as pd
from bit2me_cli_utilities.infrastructure.services.remote.bit2me_remote_service import (
    Bit2MeRemoteService,
)
from bit2me_cli_utilities.domain.global_summary import GlobalSummary
from datetime import datetime, UTC
from httpx import Client
import pydash


class GlobalSummaryService:
    def __init__(self) -> None:
        self._bit2me_remote_service = Bit2MeRemoteService()

    def get_global_summary(self) -> GlobalSummary:
        """
        Retrieves the global summary of Bit2Me transactions.
        This method currently processes local Excel files to calculate total deposits,
        withdrawals, and current value.
        """
        total_deposits = 0.0
        withdrawls = 0.0
        with self._bit2me_remote_service.get_http_client() as client:
            account_info = self._bit2me_remote_service.get_account_info(client=client)
            for current_year in range(
                account_info.registration_date.year, datetime.now(UTC).year + 1
            ):
                current_excel_file_content = (
                    self._bit2me_remote_service.get_accounting_summary_by_year(
                        year=str(current_year), client=client
                    )
                )
                df = pd.read_excel(
                    current_excel_file_content, header=1, sheet_name=None
                )
                for _, sheet_data in df.items():
                    filtered_df = sheet_data[sheet_data["Operation type"] == "Deposit"]
                    total_deposits += filtered_df["From amount"].sum()

                    filtered_df = sheet_data[
                        sheet_data["Operation type"] == "Withdrawal"
                    ]
                    withdrawls += filtered_df["From amount"].sum()

            global_summary = GlobalSummary(
                total_deposits=total_deposits,
                withdrawls=withdrawls,
                current_value=self._calculate_current_value(client),
            )

            return global_summary

    def _calculate_current_value(self, client: Client | None = None) -> float:
        balances = self._bit2me_remote_service.retrieve_porfolio_balance(
            user_currency="eur", client=client
        )
        balances_by_service_name = pydash.group_by(balances, lambda b: b.service_name)
        current_value = round(
            pydash.sum_(
                [
                    current_balance.total.converted_balance.value
                    for current_balance in balances_by_service_name.get("all", [])
                ]
            ),
            ndigits=2,
        )

        return current_value
