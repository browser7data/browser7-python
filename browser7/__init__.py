"""
Browser7 Python SDK

Official Python client for the Browser7 web scraping and rendering API.
"""

__version__ = "0.1.0a1"
__author__ = "Browser7"
__email__ = "support@browser7.com"
__url__ = "https://browser7.com"

from ._client import Browser7
from ._async_client import AsyncBrowser7
from ._types import AccountBalance, Region, RegionsResponse, RenderResult
from ._base import wait_for_click, wait_for_delay, wait_for_selector, wait_for_text

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
]
