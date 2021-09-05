from selenium import webdriver
import requests
from assertpy import assert_that


def test_get_all_airports():
    response = requests.get('https://reqres.in/api/users?page=2')
    data = response.json().get('data')

    assert response.status_code == 200
    assert len(data) > 5

