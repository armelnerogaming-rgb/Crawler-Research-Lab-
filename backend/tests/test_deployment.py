import pytest
from fastapi import HTTPException
from app.main import check_allowed_host, require_api_token


def test_missing_token_blocks_production(monkeypatch):
    monkeypatch.setenv('CRAWLER_REQUIRE_AUTH', '1')
    monkeypatch.delenv('CRAWLER_API_TOKEN', raising=False)
    with pytest.raises(HTTPException) as error:
        require_api_token()
    assert error.value.status_code == 503


def test_invalid_bearer_token_is_rejected(monkeypatch):
    monkeypatch.setenv('CRAWLER_API_TOKEN', 'expected-secret')
    with pytest.raises(HTTPException) as error:
        require_api_token('Bearer wrong-secret')
    assert error.value.status_code == 401
    require_api_token('Bearer expected-secret')


def test_host_allowlist_is_enforced(monkeypatch):
    monkeypatch.setenv('CRAWL_ALLOWED_HOSTS', 'example.org,www.example.org')
    check_allowed_host('example.org')
    with pytest.raises(ValueError):
        check_allowed_host('unexpected.example')


def test_render_requires_host_allowlist(monkeypatch):
    monkeypatch.setenv('RENDER', 'true')
    monkeypatch.delenv('CRAWL_ALLOWED_HOSTS', raising=False)
    with pytest.raises(ValueError):
        check_allowed_host('example.com')


def test_full_website_url_in_allowlist(monkeypatch):
    monkeypatch.setenv('CRAWL_ALLOWED_HOSTS', 'https://www.scrapethissite.com/pages/')
    check_allowed_host('www.scrapethissite.com')
    with pytest.raises(ValueError, match='not in the configured allowlist'):
        check_allowed_host('scrapethissite.com')


def test_multiple_allowlist_formats(monkeypatch):
    monkeypatch.setenv('CRAWL_ALLOWED_HOSTS', 'https://example.com/path, www.scrapethissite.com')
    check_allowed_host('example.com')
    check_allowed_host('www.scrapethissite.com')
