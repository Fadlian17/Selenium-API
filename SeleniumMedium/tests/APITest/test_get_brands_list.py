import requests
import pytest

def test_get_brands_list_success():
    """Test positive: Mendapatkan list brand"""
    url = "https://automationexercise.com/api/brandsList"
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert "brands" in data
    assert isinstance(data["brands"], list)

def test_get_brands_list_method_not_allowed():
    """Test negative: Method POST tidak diizinkan pada endpoint ini"""
    url = "https://automationexercise.com/api/brandsList"
    response = requests.post(url)
    assert response.status_code == 405
    assert "This request method is not supported" in response.text
