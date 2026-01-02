"""Shared HTTP client for external API integrations."""

import time
from typing import Any, Dict, Optional

import httpx

from src.api.client import NPSAPIError
from src.api.retry import RetryableHTTPClient, RetryConfig
from src.utils.logging import get_logger, log_api_request, log_api_response

logger = get_logger(__name__)


class ExternalAPIClient:
    """Reusable HTTP client for external API services."""

    def __init__(
        self,
        base_url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: float = 20.0,
        enable_retry: bool = True,
        max_retries: int = 2,
    ):
        self.base_url = base_url.rstrip("/")
        base_client = httpx.Client(
            base_url=self.base_url,
            headers=headers or {},
            timeout=timeout,
            follow_redirects=True,
        )

        if enable_retry:
            retry_config = RetryConfig(
                max_retries=max_retries,
                initial_delay=1.0,
                max_delay=30.0,
                exponential_base=2.0,
            )
            self.client = RetryableHTTPClient(base_client, retry_config)
            logger.info("retry_enabled", max_retries=max_retries)
        else:
            self.client = base_client

        logger.info("external_api_client_initialized", base_url=self.base_url)

    def close(self) -> None:
        """Close the underlying HTTP client."""
        if isinstance(self.client, RetryableHTTPClient):
            self.client.client.close()
        else:
            self.client.close()

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            error_message = f"HTTP {e.response.status_code} error"
            error_details = {"url": str(e.request.url)}

            try:
                error_data = e.response.json()
                if isinstance(error_data, dict):
                    error_message = error_data.get("message", error_message)
                    error_details.update(error_data)
            except Exception:
                error_details["response_text"] = e.response.text[:500]

            logger.error(
                "external_api_request_failed",
                error=error_message,
                status_code=e.response.status_code,
                url=str(e.request.url),
            )

            raise NPSAPIError(
                message=error_message,
                status_code=e.response.status_code,
                error_type="http_error",
                details=error_details,
            )

        try:
            return response.json()
        except Exception as e:
            logger.error("external_response_parse_failed", error=str(e))
            raise NPSAPIError(
                message="Failed to parse API response",
                status_code=response.status_code,
                error_type="parse_error",
                details={"error": str(e), "response_text": response.text[:500]},
            )

    def get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        log_api_request(logger, "GET", url, params)

        start_time = time.time()
        status_code = None
        error_msg = None

        try:
            response = self.client.get(endpoint.lstrip("/"), params=params)
            status_code = response.status_code
            duration_ms = (time.time() - start_time) * 1000
            log_api_response(logger, "GET", url, status_code, duration_ms)
            return self._handle_response(response)
        except httpx.TimeoutException:
            duration_ms = (time.time() - start_time) * 1000
            error_msg = "Request timed out"
            log_api_response(logger, "GET", url, 0, duration_ms, error=error_msg)
            raise NPSAPIError(
                message=error_msg,
                error_type="timeout_error",
                details={"url": url},
            )
        except httpx.NetworkError as e:
            duration_ms = (time.time() - start_time) * 1000
            error_msg = f"Network error: {str(e)}"
            log_api_response(logger, "GET", url, 0, duration_ms, error=error_msg)
            raise NPSAPIError(
                message="Network error occurred",
                error_type="network_error",
                details={"url": url, "error": str(e)},
            )
        except NPSAPIError:
            raise
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            error_msg = f"Unexpected error: {str(e)}"
            log_api_response(logger, "GET", url, 0, duration_ms, error=error_msg)
            raise NPSAPIError(
                message="Unexpected error occurred",
                error_type="unknown_error",
                details={"error": str(e), "url": url},
            )
