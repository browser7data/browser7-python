"""Shared helpers, payload building, and wait action functions."""

import gzip
import base64
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from ._errors import (
    Browser7Error,
    AuthenticationError,
    ValidationError,
    RateLimitError,
    InsufficientBalanceError,
    RenderError,
)


def _raise_api_error(status_code: int, response_text: str, context: str) -> None:
    """Parse response text and raise the appropriate typed error.

    Args:
        status_code: HTTP status code.
        response_text: Raw response body text.
        context: Description of the operation (e.g., 'Failed to start render').
    """
    body = None
    try:
        body = json.loads(response_text)
    except (json.JSONDecodeError, TypeError):
        pass

    api_message = (body.get('message') if body else None) or response_text
    message = f"{context}: {status_code} {api_message}"

    if status_code == 400:
        raise ValidationError(message, status_code, body)
    elif status_code in (401, 403):
        raise AuthenticationError(message, status_code, body)
    elif status_code == 402:
        raise InsufficientBalanceError(message, status_code, body)
    elif status_code == 422:
        raise RenderError(
            message, status_code, body,
            body.get('errorCode') if body else None,
            body.get('id') if body else None,
            body.get('billable') if body else None,
        )
    elif status_code == 429:
        raise RateLimitError(message, status_code, body)
    else:
        raise Browser7Error(message, status_code, body)

_VERSION = "1.0.0"
USER_AGENT = f"browser7-python/{_VERSION}"


def _build_payload(
    url: str,
    country_code: Optional[str],
    city: Optional[str],
    wait_for: Optional[List[Dict[str, Any]]],
    captcha: Optional[str],
    block_images: Optional[bool],
    fetch_urls: Optional[List[str]],
    include_screenshot: Optional[bool],
    screenshot_format: Optional[str],
    screenshot_quality: Optional[int],
    screenshot_full_page: Optional[bool],
    debug: Optional[bool] = None,
    force_new_proxy: Optional[bool] = None,
) -> Dict[str, Any]:
    """Build the camelCase API request payload from Python snake_case params."""
    payload: Dict[str, Any] = {'url': url}
    if country_code is not None:
        payload['countryCode'] = country_code
    if city is not None:
        payload['city'] = city
    if wait_for is not None:
        payload['waitFor'] = wait_for
    if captcha is not None:
        payload['captcha'] = captcha
    if block_images is not None:
        payload['blockImages'] = block_images
    if fetch_urls is not None:
        payload['fetchUrls'] = fetch_urls
    if include_screenshot is not None:
        payload['includeScreenshot'] = include_screenshot
    if screenshot_format is not None:
        payload['screenshotFormat'] = screenshot_format
    if screenshot_quality is not None:
        payload['screenshotQuality'] = screenshot_quality
    if screenshot_full_page is not None:
        payload['screenshotFullPage'] = screenshot_full_page
    if debug is not None:
        payload['debug'] = debug
    if force_new_proxy is not None:
        payload['forceNewProxy'] = force_new_proxy
    return payload


def _decompress_result(data: Dict[str, Any]) -> Dict[str, Any]:
    """Decompress gzipped HTML and fetchResponses in the API response."""
    if data.get('html'):
        try:
            data['html'] = gzip.decompress(base64.b64decode(data['html'])).decode('utf-8')
        except Exception:
            pass

    if data.get('fetchResponses'):
        try:
            data['fetchResponses'] = json.loads(
                gzip.decompress(base64.b64decode(data['fetchResponses'])).decode('utf-8')
            )
        except Exception:
            pass

    return data


def _now() -> str:
    """Return current UTC time as ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Wait action helpers
# ---------------------------------------------------------------------------

def wait_for_delay(duration: int) -> Dict[str, Any]:
    """
    Create a delay wait action.

    Args:
        duration: Duration in milliseconds (100-60000)

    Returns:
        Wait action dictionary

    Example:
        >>> wait_for_delay(3000)  # Wait 3 seconds
    """
    return {'type': 'delay', 'duration': duration}


def wait_for_selector(
    selector: str,
    state: str = 'visible',
    timeout: int = 30000,
) -> Dict[str, Any]:
    """
    Create a selector wait action.

    Args:
        selector: CSS selector to wait for
        state: Element state ('visible', 'hidden', 'attached')
        timeout: Timeout in milliseconds (1000-60000)

    Returns:
        Wait action dictionary

    Example:
        >>> wait_for_selector('.main-content', state='visible', timeout=10000)
    """
    return {'type': 'selector', 'selector': selector, 'state': state, 'timeout': timeout}


def wait_for_text(
    text: str,
    selector: Optional[str] = None,
    timeout: int = 30000,
) -> Dict[str, Any]:
    """
    Create a text wait action.

    Args:
        text: Text to wait for
        selector: Optional CSS selector to limit search scope
        timeout: Timeout in milliseconds (1000-60000)

    Returns:
        Wait action dictionary

    Example:
        >>> wait_for_text('In Stock', selector='.availability', timeout=10000)
    """
    action: Dict[str, Any] = {'type': 'text', 'text': text, 'timeout': timeout}
    if selector is not None:
        action['selector'] = selector
    return action


def wait_for_click(
    selector: str,
    timeout: int = 30000,
) -> Dict[str, Any]:
    """
    Create a click wait action.

    Args:
        selector: CSS selector of element to click
        timeout: Timeout in milliseconds (1000-60000)

    Returns:
        Wait action dictionary

    Example:
        >>> wait_for_click('.cookie-accept', timeout=5000)
    """
    return {'type': 'click', 'selector': selector, 'timeout': timeout}
