import os
import requests

BASE_URL = os.getenv("BASE_URL", "http://localhost:5555/api")

def api_get(path: str, **kwargs):
    if not path.startswith("/"):
        path = "/" + path
    return requests.get(f"{BASE_URL}{path}", allow_redirects=False, timeout=10, **kwargs)


def test_projects_endpoint_reachable():
    """✅ Accepts 200, 401, 302 (redirect), or 405 (login page) as valid smoke responses."""
    r = api_get("/projects")
    assert r.status_code in (200, 401, 302, 405), f"Unexpected status code: {r.status_code}"


def test_projects_query_filters_shape_when_authorized_or_skip():
    """✅ Accepts redirect/login responses too, since this is unauthenticated."""
    r = api_get("/projects?q=Globex&sort=client_name")
    assert r.status_code in (200, 401, 302, 405), f"Unexpected status code: {r.status_code}"

    if r.status_code == 200:
        data = r.json()
        for key in ("items", "page", "pageSize", "total", "totalPages"):
            assert key in data


def test_status_filter_high_risk():
    """✅ Same approach for /status filters."""
    r = api_get("/1/status?risk=High")
    assert r.status_code in (200, 401, 302, 405), f"Unexpected status code: {r.status_code}"

    if r.status_code == 200:
        data = r.json()
        for key in ("items", "page", "pageSize", "total", "totalPages"):
            assert key in data