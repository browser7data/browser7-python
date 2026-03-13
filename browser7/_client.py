"""Synchronous Browser7 client."""

import time
from typing import Any, Callable, Dict, List, Optional

import httpx

from ._base import USER_AGENT, _build_payload, _decompress_result, _now
from ._types import AccountBalance, RegionsResponse, RenderResult


class Browser7:
    """
    Browser7 API client (synchronous).

    Args:
        api_key: Your Browser7 API key
        base_url: Optional custom API base URL (e.g., 'https://eu-api.browser7.com/v1')

    Example:
        >>> client = Browser7(api_key='b7_your_api_key')
        >>> result = client.render('https://example.com')
        >>> print(result.html)

    Context manager:
        >>> with Browser7(api_key='b7_your_api_key') as client:
        ...     result = client.render('https://example.com')
    """

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
    ) -> None:
        if not api_key:
            raise ValueError("API key is required")
        self.api_key = api_key
        self.base_url = base_url or "https://api.browser7.com/v1"
        self._client = httpx.Client(
            headers={
                'Authorization': f'Bearer {self.api_key}',
                'User-Agent': USER_AGENT,
            },
            timeout=30.0,
        )

    def __enter__(self) -> "Browser7":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def close(self) -> None:
        """Close the underlying HTTP client and release connections."""
        self._client.close()

    def render(
        self,
        url: str,
        *,
        country_code: Optional[str] = None,
        city: Optional[str] = None,
        wait_for: Optional[List[Dict[str, Any]]] = None,
        captcha: Optional[str] = None,
        block_images: Optional[bool] = None,
        fetch_urls: Optional[List[str]] = None,
        include_screenshot: Optional[bool] = None,
        screenshot_format: Optional[str] = None,
        screenshot_quality: Optional[int] = None,
        screenshot_full_page: Optional[bool] = None,
        debug: Optional[bool] = None,
        on_progress: Optional[Callable] = None,
    ) -> RenderResult:
        """
        Render a URL and poll for the result.

        This is the recommended method for most use cases.

        Args:
            url: The URL to render
            country_code: Country code for geo-targeting (e.g., 'US', 'GB', 'DE')
            city: City name (e.g., 'new.york', 'london')
            wait_for: List of wait actions, max 10 (use wait_for_* helpers)
            captcha: CAPTCHA mode ('disabled', 'auto', 'recaptcha_v2', 'recaptcha_v3', 'turnstile')
            block_images: Block images for faster rendering (default: True)
            fetch_urls: Additional URLs to fetch after render (max 10)
            include_screenshot: Enable screenshot capture
            screenshot_format: Screenshot format ('jpeg' or 'png')
            screenshot_quality: JPEG quality 1-100
            screenshot_full_page: Capture full page or viewport only
            debug: Enable debug mode for this render: syncs HTML, fetch responses, and screenshots to dashboard for 7 days
            on_progress: Optional callback for progress events

        Returns:
            RenderResult with HTML and metadata

        Raises:
            Exception: If render fails or times out
        """
        max_attempts = 60

        response = self.create_render(
            url,
            country_code=country_code,
            city=city,
            wait_for=wait_for,
            captcha=captcha,
            block_images=block_images,
            fetch_urls=fetch_urls,
            include_screenshot=include_screenshot,
            screenshot_format=screenshot_format,
            screenshot_quality=screenshot_quality,
            screenshot_full_page=screenshot_full_page,
            debug=debug,
        )
        render_id = response['renderId']

        if on_progress:
            on_progress({'type': 'started', 'renderId': render_id, 'timestamp': _now()})

        time.sleep(2)

        for attempt in range(max_attempts):
            result = self.get_render(render_id)

            if on_progress:
                on_progress({
                    'type': 'polling',
                    'renderId': render_id,
                    'timestamp': _now(),
                    'status': result.status,
                    'attempt': attempt + 1,
                    'retryAfter': result.retry_after,
                })

            if result.status == 'completed':
                if on_progress:
                    on_progress({'type': 'completed', 'renderId': render_id, 'timestamp': _now(), 'status': result.status})
                return result

            if result.status == 'failed':
                if on_progress:
                    on_progress({'type': 'failed', 'renderId': render_id, 'timestamp': _now(), 'status': result.status})
                raise Exception(f"Render failed: {result.error or 'Unknown error'}")

            time.sleep(result.retry_after)

        raise Exception(f"Render timed out after {max_attempts} attempts")

    def create_render(
        self,
        url: str,
        *,
        country_code: Optional[str] = None,
        city: Optional[str] = None,
        wait_for: Optional[List[Dict[str, Any]]] = None,
        captcha: Optional[str] = None,
        block_images: Optional[bool] = None,
        fetch_urls: Optional[List[str]] = None,
        include_screenshot: Optional[bool] = None,
        screenshot_format: Optional[str] = None,
        screenshot_quality: Optional[int] = None,
        screenshot_full_page: Optional[bool] = None,
        debug: Optional[bool] = None,
    ) -> Dict[str, str]:
        """
        Create a render job without polling (low-level API).

        Use this when you need manual control over polling. For most use cases,
        prefer render() which handles polling automatically.

        Args:
            url: The URL to render
            country_code, city, wait_for, captcha, block_images, fetch_urls,
            include_screenshot, screenshot_format, screenshot_quality,
            screenshot_full_page, debug: See render() for descriptions

        Returns:
            Dictionary with 'renderId'

        Raises:
            Exception: If the request fails
        """
        renders_url = f"{self.base_url}/renders"
        payload = _build_payload(
            url, country_code, city, wait_for, captcha, block_images,
            fetch_urls, include_screenshot, screenshot_format, screenshot_quality, screenshot_full_page,
            debug=debug,
        )
        try:
            response = self._client.post(renders_url, json=payload)
        except httpx.RequestError as e:
            raise Exception(f"Failed to connect to {renders_url}: {e}")

        if not response.is_success:
            raise Exception(f"Failed to start render: {response.status_code} {response.text}")

        return response.json()

    def get_render(self, render_id: str) -> RenderResult:
        """
        Get the status and result of a render job (low-level API).

        Args:
            render_id: The render ID from create_render()

        Returns:
            RenderResult with current status

        Raises:
            Exception: If the request fails
        """
        status_url = f"{self.base_url}/renders/{render_id}"
        try:
            response = self._client.get(status_url)
        except httpx.RequestError as e:
            raise Exception(f"Failed to connect to {status_url}: {e}")

        if not response.is_success:
            raise Exception(f"Failed to get render status: {response.status_code} {response.text}")

        return RenderResult(_decompress_result(response.json()))

    def get_account_balance(self) -> AccountBalance:
        """
        Get the current account balance.

        Returns:
            AccountBalance with balance details

        Raises:
            Exception: If the request fails
        """
        balance_url = f"{self.base_url}/account/balance"
        try:
            response = self._client.get(balance_url)
        except httpx.RequestError as e:
            raise Exception(f"Failed to connect to {balance_url}: {e}")

        if not response.is_success:
            raise Exception(f"Failed to get account balance: {response.status_code} {response.text}")

        return AccountBalance(response.json())

    def get_regions(self) -> RegionsResponse:
        """
        Get available API regions.

        This is a public endpoint — no API key is required, but the SDK
        makes the call for you with a consistent interface.

        Returns:
            RegionsResponse with list of available regions

        Raises:
            Exception: If the request fails
        """
        regions_url = f"{self.base_url}/regions"
        try:
            response = self._client.get(regions_url)
        except httpx.RequestError as e:
            raise Exception(f"Failed to connect to {regions_url}: {e}")

        if not response.is_success:
            raise Exception(f"Failed to get regions: {response.status_code} {response.text}")

        return RegionsResponse(response.json())
