import requests
import pytest
import logging

def is_valid_product(product):
    """Validasi struktur data produk"""
    required_keys = ["id", "name", "price", "brand"]
    return all(key in product for key in required_keys)

@pytest.fixture(scope="module")
def api_base_url():
    return "https://automationexercise.com/api"

@pytest.fixture(scope="function")
def log_response():
    logger = logging.getLogger("api_test")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler("api_test.log")
    logger.addHandler(handler)
    yield logger
    logger.removeHandler(handler)


def test_get_products_list_success(api_base_url, log_response):
    """Test positive: Mendapatkan list produk dan validasi struktur data"""
    url = f"{api_base_url}/productsList"
    response = requests.get(url, timeout=10)
    log_response.info(f"GET {url} - Status: {response.status_code}")
    assert response.status_code == 200
    data = response.json()
    assert "products" in data
    assert isinstance(data["products"], list)
    # Validasi minimal 1 produk dan struktur data
    assert len(data["products"]) > 0
    for product in data["products"]:
        assert is_valid_product(product)


def test_get_products_list_method_not_allowed(api_base_url, log_response):
    """Test negative: Method POST tidak diizinkan pada endpoint ini"""
    url = f"{api_base_url}/productsList"
    response = requests.post(url, timeout=10)
    log_response.info(f"POST {url} - Status: {response.status_code}")
    assert response.status_code == 405
    assert "This request method is not supported" in response.text


def test_get_products_list_timeout(api_base_url, log_response):
    """Test robust: Simulasi timeout dan error handling"""
    url = f"{api_base_url}/productsList"
    try:
        response = requests.get(url, timeout=0.001)
        log_response.info(f"Timeout test: {response.status_code}")
        assert False, "Request seharusnya timeout"
    except requests.exceptions.Timeout:
        log_response.info("Timeout terjadi sesuai ekspektasi")
        assert True


def test_get_products_list_invalid_url(log_response):
    """Test robust: Endpoint tidak valid"""
    url = "https://automationexercise.com/api/productsListInvalid"
    response = requests.get(url, timeout=10)
    log_response.info(f"GET {url} - Status: {response.status_code}")
    assert response.status_code == 404
