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


def test_allowlist_accepts_pasted_full_url(monkeypatch):
    monkeypatch.setenv('CRAWL_ALLOWED_HOSTS', 'https://www.scrapethissite.com/pages/')
    check_allowed_host('www.scrapethissite.com')
    with pytest.raises(ValueError):
        check_allowed_host('other.scrapethissite.com')


def test_allowlist_rejects_credentials_and_nonstandard_ports(monkeypatch):
    for value in ['https://user:password@example.org/', 'https://example.org:8080/']:
        monkeypatch.setenv('CRAWL_ALLOWED_HOSTS', value)
        with pytest.raises(ValueError):
            check_allowed_host('example.org')
