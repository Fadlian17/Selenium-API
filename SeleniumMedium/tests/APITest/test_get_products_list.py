import requests
import pytest

def test_get_products_list_success():
    """Test positive: Mendapatkan list produk"""
    url = "https://automationexercise.com/api/productsList"
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert "products" in data
    assert isinstance(data["products"], list)


def test_get_products_list_method_not_allowed():
    """Test negative: Method POST tidak diizinkan pada endpoint ini"""
    url = "https://automationexercise.com/api/productsList"
    response = requests.post(url)
    assert response.status_code == 405
    assert "This request method is not supported" in response.text
