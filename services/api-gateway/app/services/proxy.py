"""
HTTP reverse proxy — forwards requests to the Django monolith.

Transparently proxies all headers, body, query params, and
returns the monolith's response unchanged.
"""

import logging

import httpx

from ..config import settings

logger = logging.getLogger(__name__)

# Long-lived async client for connection pooling
_client: httpx.AsyncClient | None = None


async def get_proxy_client() -> httpx.AsyncClient:
    """Get or create the proxy HTTP client."""
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(
            base_url=settings.MONOLITH_URL,
            timeout=httpx.Timeout(120.0, connect=10.0),
            follow_redirects=False,
        )
    return _client


async def close_proxy_client() -> None:
    """Close the proxy client."""
    global _client
    if _client and not _client.is_closed:
        await _client.aclose()
        _client = None


async def proxy_request(
    method: str,
    path: str,
    headers: dict,
    body: bytes | None = None,
    query_string: str = "",
) -> httpx.Response:
    """
    Proxy an HTTP request to the monolith.

    Args:
        method: HTTP method (GET, POST, etc.)
        path: URL path (e.g. /api/v1/words/)
        headers: Request headers to forward
        body: Request body bytes
        query_string: URL query string

    Returns:
        httpx.Response from the monolith
    """
    client = await get_proxy_client()

    url = path
    if query_string:
        url = f"{path}?{query_string}"

    # Filter out hop-by-hop headers
    proxy_headers = {
        k: v for k, v in headers.items()
        if k.lower() not in ("host", "connection", "transfer-encoding", "keep-alive")
    }

    response = await client.request(
        method=method,
        url=url,
        headers=proxy_headers,
        content=body,
    )

    return response
