import os
from typing import Any

import requests  # type: ignore[import-untyped]
from zabbix_utils import ZabbixAPI  # type: ignore[import-untyped]


class ZabbixClient:
    def __init__(
        self,
        url: str | None = None,
        token: str | None = None,
        user: str | None = None,
        password: str | None = None,
        timeout: int = 30,
    ) -> None:
        self.url: str = url or os.environ.get("ZABBIX_URL") or ""
        self.token = token or os.environ.get("ZABBIX_TOKEN")
        self.user = user or os.environ.get("ZABBIX_USER")
        self.password = password or os.environ.get("ZABBIX_PASSWORD")

        if not self.url:
            raise ValueError("ZABBIX_URL is required")

        if not self.token and not (self.user and self.password):
            raise ValueError(
                "Either ZABBIX_TOKEN or ZABBIX_USER/ZABBIX_PASSWORD is required"
            )

        self.timeout = timeout
        self._api: ZabbixAPI | None = None

    @property
    def api(self) -> ZabbixAPI:
        if self._api is None:
            self._api = ZabbixAPI(
                url=self.url,
                token=self.token,
                user=self.user,
                password=self.password,
                timeout=self.timeout,
            )
        return self._api

    def call_method(
        self, method: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        try:
            return self.api.call(method, params or {})  # type: ignore[no-any-return]
        except requests.exceptions.Timeout as e:
            raise TimeoutError(f"Request timed out after {self.timeout}s: {e}") from e
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(f"Failed to connect to {self.url}: {e}") from e
        except requests.exceptions.HTTPError as e:
            raise RuntimeError(f"HTTP error: {e}") from e
        except Exception as e:
            raise RuntimeError(f"Zabbix API error: {e}") from e


_client: ZabbixClient | None = None


def get_client(
    url: str | None = None,
    token: str | None = None,
    user: str | None = None,
    password: str | None = None,
) -> ZabbixClient:
    global _client
    _client = ZabbixClient(
        url=url,
        token=token,
        user=user,
        password=password,
    )
    return _client


def client() -> ZabbixClient:
    if _client is None:
        return get_client()
    return _client
