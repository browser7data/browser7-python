"""
Browser7 Python SDK

Official Python client for the Browser7 web scraping and rendering API.
"""

__version__ = "1.0.0"
__author__ = "Browser7"
__email__ = "support@browser7.com"
__url__ = "https://browser7.com"

from ._client import Browser7
from ._async_client import AsyncBrowser7
from ._types import AccountBalance, Region, RegionsResponse, RenderResult
from ._base import wait_for_click, wait_for_delay, wait_for_selector, wait_for_text
from ._errors import (
    Browser7Error,
    AuthenticationError,
    ValidationError,
    RateLimitError,
    InsufficientBalanceError,
    RenderError,
)

__all__ = [
    # Clients
    'Browser7',
    'AsyncBrowser7',
    # Types
    'RenderResult',
    'AccountBalance',
    'Region',
    'RegionsResponse',
    # Wait action helpers
    'wait_for_delay',
    'wait_for_selector',
    'wait_for_text',
    'wait_for_click',
    # Error classes
    'Browser7Error',
    'AuthenticationError',
    'ValidationError',
    'RateLimitError',
    'InsufficientBalanceError',
    'RenderError',
]
