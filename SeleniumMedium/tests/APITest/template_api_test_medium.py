import requests
import pytest
import logging

# Template dasar untuk API Test level medium
@pytest.fixture(scope="module")
def api_base_url():
    return "https://automationexercise.com/api"

@pytest.fixture(scope="function")
def log_response():
    logger = logging.getLogger("api_test")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler("api_test_medium.log")
    logger.addHandler(handler)
    yield logger
    logger.removeHandler(handler)


def test_api_positive(api_base_url, log_response):
    """Contoh test positif: GET productsList"""
    url = f"{api_base_url}/productsList"
    response = requests.get(url, timeout=10)
    log_response.info(f"GET {url} - Status: {response.status_code}")
    assert response.status_code == 200
    data = response.json()
    assert "products" in data
    assert isinstance(data["products"], list)


def test_api_negative(api_base_url, log_response):
    """Contoh test negatif: POST ke productsList (method tidak diizinkan)"""
    url = f"{api_base_url}/productsList"
    response = requests.post(url, timeout=10)
    log_response.info(f"POST {url} - Status: {response.status_code}")
    assert response.status_code == 405
    assert "This request method is not supported" in response.text


def test_api_timeout(api_base_url, log_response):
    """Contoh test robust: Simulasi timeout"""
    url = f"{api_base_url}/productsList"
    try:
        requests.get(url, timeout=0.001)
        assert False, "Request seharusnya timeout"
    except requests.exceptions.Timeout:
        log_response.info("Timeout terjadi sesuai ekspektasi")
        assert True


def test_api_invalid_url(log_response):
    """Contoh test robust: Endpoint tidak valid"""
    url = "https://automationexercise.com/api/invalidEndpoint"
    response = requests.get(url, timeout=10)
    log_response.info(f"GET {url} - Status: {response.status_code}")
    assert response.status_code == 404

# Tambahkan test lain sesuai kebutuhan, misal: validasi struktur data, chaining, dsb.
