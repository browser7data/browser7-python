"""Type definitions for the Browser7 SDK."""

from typing import Any, Dict, List, Optional


class RenderResult:
    """
    Result from a render operation.

    Attributes:
        status: Render status ('completed', 'processing', 'failed')
        html: Rendered HTML content (automatically decompressed)
        screenshot: Base64-encoded screenshot image (if include_screenshot was True)
        load_strategy: Load strategy used for rendering
        selected_city: City information used for the render
        bandwidth_metrics: Network bandwidth statistics
        captcha: CAPTCHA detection and handling info
        timing_breakdown: Performance timing breakdown
        fetch_responses: Additional fetch responses (automatically decompressed)
        retry_after: Server-suggested retry interval in seconds
        error: Error message if status is 'failed'
    """

    __slots__ = (
        'status', 'html', 'screenshot', 'load_strategy', 'selected_city',
        'bandwidth_metrics', 'captcha', 'timing_breakdown', 'fetch_responses',
        'retry_after', 'error',
    )

    def __init__(self, data: Dict[str, Any]) -> None:
        self.status: Optional[str] = data.get('status')
        self.html: Optional[str] = data.get('html')
        self.screenshot: Optional[str] = data.get('screenshot')
        self.load_strategy: Optional[str] = data.get('loadStrategy')
        self.selected_city: Optional[Dict[str, Any]] = data.get('selectedCity')
        self.bandwidth_metrics: Optional[Dict[str, Any]] = data.get('bandwidthMetrics')
        self.captcha: Optional[Dict[str, Any]] = data.get('captcha')
        self.timing_breakdown: Optional[Dict[str, Any]] = data.get('timingBreakdown')
        self.fetch_responses: Optional[List[Any]] = data.get('fetchResponses')
        self.retry_after: float = data.get('retryAfter', 1)
        self.error: Optional[str] = data.get('error')

    def __repr__(self) -> str:
        return f"RenderResult(status='{self.status}')"


class AccountBalance:
    """
    Account balance information.

    Attributes:
        total_balance_cents: Total balance in cents (1 cent = 1 render)
        total_balance_formatted: Total balance formatted as USD (e.g., '$13.00')
        breakdown: Balance breakdown by type (paid, free, bonus).
            Each has 'cents' (int) and 'formatted' (str) keys.
    """

    __slots__ = ('total_balance_cents', 'total_balance_formatted', 'breakdown')

    def __init__(self, data: Dict[str, Any]) -> None:
        self.total_balance_cents: int = data.get('totalBalanceCents', 0)
        self.total_balance_formatted: str = data.get('totalBalanceFormatted', '$0.00')
        self.breakdown: Dict[str, Any] = data.get('breakdown', {
            'paid': {'cents': 0, 'formatted': '$0.00'},
            'free': {'cents': 0, 'formatted': '$0.00'},
            'bonus': {'cents': 0, 'formatted': '$0.00'},
        })

    def __repr__(self) -> str:
        return (
            f"AccountBalance(total={self.total_balance_formatted}, "
            f"renders_remaining={self.total_balance_cents})"
        )


class Region:
    """
    An available API region.

    Attributes:
        code: Region code (e.g., 'eu', 'ca', 'sg')
        name: Human-readable region name (e.g., 'Europe')
        status: Region status ('active', 'maintenance', 'inactive')
    """

    __slots__ = ('code', 'name', 'status')

    def __init__(self, data: Dict[str, Any]) -> None:
        self.code: str = data.get('code', '')
        self.name: str = data.get('name', '')
        self.status: str = data.get('status', '')

    def __repr__(self) -> str:
        return f"Region(code='{self.code}', name='{self.name}', status='{self.status}')"


class RegionsResponse:
    """
    Response from get_regions().

    Attributes:
        regions: List of available API regions
    """

    __slots__ = ('regions',)

    def __init__(self, data: Dict[str, Any]) -> None:
        self.regions: List[Region] = [Region(r) for r in data.get('regions', [])]

    def __repr__(self) -> str:
        return f"RegionsResponse(regions={self.regions})"
