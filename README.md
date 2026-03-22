# Browser7 Python SDK

---

Official Python client for the [Browser7](https://browser7.com) web scraping and rendering API.

Browser7 provides geo-targeted web scraping with automatic proxy management, CAPTCHA solving, and powerful wait actions for dynamic content.

## Features

- 🌍 **Geo-Targeting** - Render pages from specific countries and cities
- 🤖 **CAPTCHA Solving** - Automatic detection and solving of reCAPTCHA and Cloudflare Turnstile
- ⏱️ **Wait Actions** - Click elements, wait for selectors, text, or delays
- 🚀 **Performance** - Block images, track bandwidth, view timing metrics
- 🔄 **Automatic Polling** - Built-in polling with progress callbacks
- 💪 **Type Hints** - Full type annotations for IDE support

## Installation

```bash
pip install browser7
```

**Requirements:** Python 3.10+

## Quick Start

```python
from browser7 import Browser7

client = Browser7(api_key='your-api-key')

# Simple render
result = client.render('https://example.com')
print(result.html)
```

## Authentication

Get your API key from the [Browser7 Dashboard](https://dashboard.browser7.com).

```python
client = Browser7(api_key='b7_your_api_key_here')
```

## Usage Examples

### Basic Rendering

```python
result = client.render('https://example.com', country_code='US')

print(result.html)              # Rendered HTML
print(result.selected_city)     # City used for rendering
```

### With Wait Actions

```python
from browser7 import wait_for_click, wait_for_selector, wait_for_delay

result = client.render(
    'https://example.com',
    country_code='GB',
    city='london',
    wait_for=[
        wait_for_click('.cookie-accept'),           # Click element
        wait_for_selector('.main-content'),          # Wait for element
        wait_for_delay(2000)                         # Wait 2 seconds
    ]
)
```

### With CAPTCHA Solving

```python
result = client.render(
    'https://protected-site.com',
    country_code='US',
    captcha='auto'  # Auto-detect and solve CAPTCHAs
)

print(result.captcha)  # CAPTCHA detection info
```

### Check Account Balance

```python
balance = client.get_account_balance()

print(f"Total: {balance.total_balance_formatted}")
print(f"Renders remaining: {balance.total_balance_cents}")
print(f"\nBreakdown:")
print(f"  Paid: {balance.breakdown['paid']['formatted']} ({balance.breakdown['paid']['cents']} renders)")
print(f"  Free: {balance.breakdown['free']['formatted']} ({balance.breakdown['free']['cents']} renders)")
print(f"  Bonus: {balance.breakdown['bonus']['formatted']} ({balance.breakdown['bonus']['cents']} renders)")
```

## API Reference

### `Browser7(api_key, base_url=None)`

Create a new Browser7 client.

**Parameters:**
- `api_key` (str, required): Your Browser7 API key
- `base_url` (str, optional): Full API base URL. Defaults to production API.

**Example:**
```python
# Production (default)
client = Browser7(api_key='your-api-key')

# Canadian endpoint
client = Browser7(
    api_key='your-api-key',
    base_url='https://ca-api.browser7.com/v1'
)
```

### `client.render(url, **options)`

Render a URL and poll for the result.

**Parameters:**
- `url` (str): The URL to render
- `country_code` (str, optional): Country code (e.g., 'US', 'GB', 'DE')
- `city` (str, optional): City name (e.g., 'new.york', 'london')
- `wait_for` (list, optional): List of wait actions (max 10)
- `captcha` (str, optional): CAPTCHA mode: 'disabled', 'auto', 'recaptcha_v2', 'recaptcha_v3', 'turnstile'
- `block_images` (bool, optional): Block images for faster rendering (default: True)
- `fetch_urls` (list, optional): Additional URLs to fetch (max 10)

**Returns:** `RenderResult` object

### `client.get_account_balance()`

Get the current account balance.

**Returns:** `AccountBalance` object

**Example:**
```python
balance = client.get_account_balance()
print(f"Total: {balance.total_balance_formatted}")
print(f"Renders remaining: {balance.total_balance_cents}")
```

**AccountBalance attributes:**
- `total_balance_cents` (int): Total balance in cents (also equals renders remaining, since 1 cent = 1 render)
- `total_balance_formatted` (str): Total balance formatted as USD currency (e.g., "$13.00")
- `breakdown` (dict): Balance breakdown by type
  - `breakdown['paid']` - Paid balance with `cents` and `formatted` keys
  - `breakdown['free']` - Free balance with `cents` and `formatted` keys
  - `breakdown['bonus']` - Bonus balance with `cents` and `formatted` keys

## Helper Functions

### `wait_for_delay(duration)`

Create a delay wait action.

```python
wait_for_delay(3000)  # Wait 3 seconds
```

### `wait_for_selector(selector, state='visible', timeout=30000)`

Create a selector wait action.

```python
wait_for_selector('.main-content', state='visible', timeout=10000)
```

### `wait_for_text(text, selector=None, timeout=30000)`

Create a text wait action.

```python
wait_for_text('In Stock', selector='.availability', timeout=10000)
```

### `wait_for_click(selector, timeout=30000)`

Create a click wait action.

```python
wait_for_click('.cookie-accept', timeout=5000)
```

## Supported Countries

AT, BE, CA, CH, CZ, DE, FR, GB, HR, HU, IT, NL, PL, SK, US

See [Browser7 Documentation](https://docs.browser7.com) for available cities per country.

## CAPTCHA Support

Browser7 supports automatic CAPTCHA detection and solving for:

- **reCAPTCHA v2** - Google's image-based CAPTCHA
- **reCAPTCHA v3** - Google's score-based CAPTCHA
- **Cloudflare Turnstile** - Cloudflare's CAPTCHA alternative

**Modes:**
- `'disabled'` (default) - Skip CAPTCHA detection (fastest)
- `'auto'` - Auto-detect and solve any CAPTCHA type
- `'recaptcha_v2'`, `'recaptcha_v3'`, `'turnstile'` - Solve specific type

## Contributing

Issues and pull requests are welcome! Please visit our [GitHub repository](https://github.com/browser7data/browser7-python).

## License

MIT

## Support

- 📧 Email: support@browser7.com
- 📚 Documentation: https://docs.browser7.com
- 🐛 Issues: https://github.com/browser7data/browser7-python/issues

## Links

- [Browser7 Website](https://browser7.com)
- [API Documentation](https://docs.browser7.com/api/overview)
- [Dashboard](https://dashboard.browser7.com)
- [Pricing](https://browser7.com/pricing)
