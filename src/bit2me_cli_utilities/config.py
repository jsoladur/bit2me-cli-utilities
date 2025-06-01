from __future__ import annotations
from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

_configuration_properties: ConfigurationProperties | None = None


class ConfigurationProperties(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        validate_default=False,
        extra="allow",
    )
    # Bit2Me API configuration
    bit2me_api_base_url: AnyUrl
    bit2me_api_key: str
    bit2me_api_secret: str


def get_configuration_properties() -> ConfigurationProperties:
    global _configuration_properties
    if _configuration_properties is None:
        _configuration_properties = ConfigurationProperties()
    return _configuration_properties
