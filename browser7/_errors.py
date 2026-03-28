"""
Browser7 SDK Error Classes.

Hierarchy::

    Browser7Error (base)          — network errors, 404, 500+, constructor validation
    ├── AuthenticationError       — 401, 403
    ├── ValidationError           — 400
    ├── RateLimitError            — 429
    ├── InsufficientBalanceError  — 402
    └── RenderError               — 422 (failed render), render() failure/timeout
"""

import re
from typing import Any, Dict, Optional


class Browser7Error(Exception):
    """Base exception for all Browser7 SDK errors.

    Args:
        message: Human-readable error message.
        status_code: HTTP status code (None for network/timeout errors).
        body: Parsed JSON response body (None for network errors).
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        body: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.body = body


class AuthenticationError(Browser7Error):
    """Raised for 401 Unauthorized and 403 Forbidden responses."""
    pass


class ValidationError(Browser7Error):
    """Raised for 400 Bad Request responses (invalid parameters)."""

    @property
    def details(self) -> Optional[Any]:
        """Validation error details from the API response."""
        if self.body is not None:
            return self.body.get('details')
        return None


class RateLimitError(Browser7Error):
    """Raised for 429 Too Many Requests responses."""

    @property
    def concurrent_limit(self) -> Optional[int]:
        """Maximum concurrent requests allowed, parsed from the error message."""
        match = re.search(r'Maximum allowed:\s*(\d+)', str(self))
        return int(match.group(1)) if match else None


class InsufficientBalanceError(Browser7Error):
    """Raised for 402 Payment Required responses."""
    pass


class RenderError(Browser7Error):
    """Raised for failed renders (422) and render polling failures/timeouts.

    Args:
        message: Human-readable error message.
        status_code: HTTP status code (None for polling failures).
        body: Parsed JSON response body.
        error_code: API error code (e.g., 'NETWORK_ERROR', 'RENDER_TIMEOUT').
        render_id: The render ID.
        billable: Whether the render was charged.
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        body: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None,
        render_id: Optional[str] = None,
        billable: Optional[bool] = None,
    ) -> None:
        super().__init__(message, status_code, body)
        self.error_code = error_code
        self.render_id = render_id
        self.billable = billable
