import requests
import pytest

def test_search_product_success():
    """Test positive: Mencari produk dengan parameter valid"""
    url = "https://automationexercise.com/api/searchProduct"
    data = {"search_product": "dress"}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    data = response.json()
    assert "products" in data
    assert isinstance(data["products"], list)

def test_search_product_missing_param():
    """Test negative: Parameter search_product tidak diisi"""
    url = "https://automationexercise.com/api/searchProduct"
    response = requests.post(url)
    assert response.status_code == 400
    assert "Bad request, search_product parameter is missing" in response.text
