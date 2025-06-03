import time
from bit2me_cli_utilities.config import get_configuration_properties
from httpx import Client, Response, Timeout
from bit2me_cli_utilities.infrastructure.services.remote.base import (
    AbstractHttpRemoteService,
)
from pydantic import RootModel
from bit2me_cli_utilities.infrastructure.dtos import AccountInfoDto, PortfolioBalanceDto
from typing import Any
from urllib.parse import urlencode
import hashlib
import hmac
import base64
import json


class Bit2MeRemoteService(AbstractHttpRemoteService):
    def __init__(self):
        self._configuration_properties = get_configuration_properties()
        self._base_url = str(self._configuration_properties.bit2me_api_base_url)
        self._api_key = self._configuration_properties.bit2me_api_key
        self._api_secret = self._configuration_properties.bit2me_api_secret

    def get_account_info(self, *, client: Client | None = None) -> AccountInfoDto:
        response = self._perform_http_request(
            url="/v1/account",
            client=client,
        )
        response.raise_for_status()
        ret = AccountInfoDto.model_validate_json(response.content)
        return ret

    def retrieve_porfolio_balance(
        self, user_currency: str, *, client: Client | None = None
    ) -> list[PortfolioBalanceDto]:
        response = self._perform_http_request(
            url="/v1/portfolio/balance",
            params={"userCurrency": user_currency.strip().upper()},
            client=client,
        )
        response.raise_for_status()  # Ensure we raise an error for bad responses
        ret = (
            RootModel[list[PortfolioBalanceDto]]
            .model_validate_json(response.content)
            .root
        )
        return ret

    def get_accounting_summary_by_year(
        self, year: str, *, client: Client | None = None
    ) -> bytes:
        response = self._perform_http_request(
            url=f"/v1/accounting/summary/{year}",
            params={
                "timeZone": "Europe/Madrid",
                "langCode": "en",
                "documentType": "xlsx",
            },
            client=client,
        )
        response.raise_for_status()  # Ensure we raise an error for bad responses
        return response.content

    def _apply_request_interceptor(
        self,
        *,
        method: str = "GET",
        url: str = "/",
        params: dict[str, Any] | None = {},
        headers: dict[str, Any] | None = {},
        body: Any | None = None,
    ) -> tuple[str, str, dict[str, Any] | None, dict[str, Any] | None]:
        params, headers = super()._apply_request_interceptor(
            method=method, url=url, params=params, headers=headers, body=body
        )
        nonce = headers["x-nonce"] = str(
            int(time.time() * 1000)
        )  # UTC timestamp in milliseconds
        headers["api-signature"] = self._generate_api_signature(
            nonce, url, params, body
        )
        return params, headers

    def _apply_response_interceptor(
        self,
        *,
        method: str = "GET",
        url: str = "/",
        params: dict[str, Any] | None = {},
        headers: dict[str, Any] | None = {},
        body: Any | None = None,
        response: Response,
    ) -> Response:
        if not response.is_success:
            raise ValueError(
                f"Bit2Me API error: HTTP {method} {self._build_full_url(url, params)} "
                + f"- Status code: {response.status_code} - {response.text}"
            )
        return super()._apply_response_interceptor(
            method=method,
            url=url,
            params=params,
            headers=headers,
            body=body,
            response=response,
        )

    def get_http_client(self) -> Client:
        return Client(
            base_url=self._base_url,
            headers={"X-API-KEY": self._api_key},
            timeout=Timeout(30, connect=5, read=120),
        )

    def _generate_api_signature(
        self,
        nonce: str,
        url: str,
        params: dict[str, Any] | None,
        body: Any,
    ) -> str:
        url = self._build_full_url(url, params)
        message_to_sign = f"{nonce}:{url}"
        if body:
            message_to_sign += f":{json.dumps(body, separators=(',', ':'))}"
        sha256_hash = hashlib.sha256()
        hash_digest = sha256_hash.update(message_to_sign.encode("utf-8"))
        hash_digest = sha256_hash.digest()
        # Create HMAC-SHA512
        hmac_obj = hmac.new(self._api_secret.encode(), hash_digest, hashlib.sha512)
        hmac_digest = base64.b64encode(hmac_obj.digest()).decode()
        return hmac_digest

    def _build_full_url(self, path: str, query_params: dict[str, any]) -> str:
        full_url = path
        if query_params:
            query_string = urlencode(query_params, doseq=True)
            full_url += "?" + query_string
        return full_url
