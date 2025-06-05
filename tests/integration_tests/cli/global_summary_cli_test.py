from pytest_httpserver import HTTPServer
from faker import Faker
from typer.testing import CliRunner
from datetime import datetime
from tests.helpers.httpserver_pytest.request_matchers import Bit2MeAPIRequestMacher
from pytest_httpserver.httpserver import HandlerType
from bit2me_cli_utilities.infrastructure.dtos.account_info_dto import AccountInfoDto


def should_make_all_expected_calls_to_bit2me_when_trailing_stop_lost(
    faker: Faker,
    integration_test_env: tuple[HTTPServer, str, str],
) -> None:
    """
    Test that all expected calls to Bit2Me are made when a trailing stop is lost.
    """
    # Mock the Bit2Me API
    httpserver, bit2me_api_key, bit2me_api_secret, *_ = integration_test_env

    _prepare_httpserver_mock(faker, httpserver, bit2me_api_key, bit2me_api_secret)

    from bit2me_cli_utilities.main import app

    runner = CliRunner()
    result = runner.invoke(app, ["global-summary", "show"])
    if result.exit_code != 0 and result.exception:
        raise result.exception

    httpserver.check_assertions()


def _prepare_httpserver_mock(
    faker: Faker, httpserver: HTTPServer, bit2me_api_key: str, bik2me_api_secret: str
) -> None:
    # Mock call to /v1/trading/order
    # Get current year and compute previous year
    previous_year = datetime.now().year - 1
    httpserver.expect(
        Bit2MeAPIRequestMacher(
            "/v1/account",
            method="GET",
        ).set_bit2me_api_key_and_secret(bit2me_api_key, bik2me_api_secret),
        handler_type=HandlerType.ONESHOT,
    ).respond_with_json(
        AccountInfoDto(
            registration_date=faker.date_time_between(
                start_date=datetime(previous_year, 1, 1),
                end_date=datetime(previous_year, 12, 31),
            )
        ).model_dump(mode="json", by_alias=True),
    )
    for current_year in range(previous_year + 1, datetime.now().year + 1):
        httpserver.expect(
            Bit2MeAPIRequestMacher(
                f"/v1/accounting/summary/{current_year}",
                method="GET",
                query_string={
                    "timeZone": "Europe/Madrid",
                    "langCode": "en",
                    "documentType": "xlsx",
                },
            ).set_bit2me_api_key_and_secret(bit2me_api_key, bik2me_api_secret),
            handler_type=HandlerType.ONESHOT,
        ).respond_with_data("")
