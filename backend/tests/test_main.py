import pytest
from app.main import normalize, validate_public

def test_reject_bad_schemes():
    for url in ['file:///etc/passwd','javascript:alert(1)','ftp://example.com','https://u:p@example.com']:
        with pytest.raises(ValueError): normalize(url)

def test_private_ip_blocked():
    for url in ['http://127.0.0.1','http://10.1.1.1','http://169.254.169.254','http://[::1]']:
        with pytest.raises(ValueError): validate_public(url)

def test_fragment_removed():
    assert normalize('https://example.com/a#section') == 'https://example.com/a'
