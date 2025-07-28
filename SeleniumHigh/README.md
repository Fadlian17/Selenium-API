# SeleniumHigh Framework

Framework testing automation yang sederhana dan modular untuk testing website dan API.

## 🚀 Fitur Utama

- **Selenium WebDriver**: Testing UI otomatis
- **API Testing**: Testing API dengan requests
- **Page Object Model**: Struktur yang modular dan mudah maintain
- **Pytest**: Framework testing yang powerful
- **HTML Reports**: Laporan test yang informatif

## 📁 Struktur Project

```
SeleniumHigh/
├── pages/           # Page Object Models
│   ├── base_page.py
│   └── home_page.py
├── api/             # API Client
│   └── api_client.py
├── tests/           # Test files
│   ├── test_simple.py
│   └── test_api_only.py
├── conftest.py      # Pytest fixtures
├── requirements.txt # Dependencies
└── pytest.ini      # Pytest configuration
```

## 🛠️ Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install ChromeDriver (Opsional)
Jika menggunakan Selenium:
```bash
# Download ChromeDriver sesuai versi Chrome Anda
# Atau gunakan webdriver-manager (otomatis)
```

## 🏃‍♂️ Cara Menjalankan Tests

### 1. Test API Saja (Tanpa Browser)
```bash
# Test API connection
python3 -c "import requests; response = requests.get('https://automationexercise.com/api/productsList', timeout=10); print(f'Status: {response.status_code}')"

# Atau jalankan test API
pytest tests/test_api_only.py -v
```

### 2. Test Selenium (Dengan Browser)
```bash
# Jalankan test sederhana
pytest tests/test_simple.py -v

# Jalankan test tertentu
pytest tests/test_simple.py::TestSimple::test_homepage_loads -v
```

### 3. Jalankan Semua Tests
```bash
pytest tests/ -v
```

### 4. Generate HTML Report
```bash
pytest tests/ --html=reports/test_report.html --self-contained-html
```

## 📝 Contoh Test

### API Test
```python
def test_api_connection(self):
    response = requests.get("https://automationexercise.com/api/productsList", timeout=10)
    assert response.status_code == 200
    print("✅ API connection successful")
```

### Selenium Test
```python
def test_homepage_loads(self, setup_browser):
    driver = setup_browser
    home_page = HomePage(driver)
    home_page.navigate_to_home()
    assert "Automation Exercise" in driver.title
    print("✅ Homepage loaded successfully")
```

## 🔧 Troubleshooting

### ChromeDriver Issues
Jika ada masalah dengan ChromeDriver:

1. **Hapus cache webdriver-manager**:
   ```bash
   rm -rf ~/.wdm
   ```

2. **Update webdriver-manager**:
   ```bash
   pip install --upgrade webdriver-manager
   ```

3. **Download ChromeDriver manual**:
   - Cek versi Chrome: `google-chrome --version`
   - Download ChromeDriver yang sesuai dari: https://chromedriver.chromium.org/

### Import Issues
Jika ada error `ModuleNotFoundError: No module named 'pages'`:

1. Pastikan berada di direktori `SeleniumHigh`
2. Pastikan semua file `__init__.py` ada
3. Jalankan dengan Python path yang benar:
   ```bash
   PYTHONPATH=. pytest tests/ -v
   ```

## 📊 Reports

Setelah menjalankan tests, laporan akan tersimpan di:
- `reports/test_report.html` - HTML report
- `screenshots/` - Screenshots jika ada error

## 🎯 Target Website

Framework ini dikonfigurasi untuk testing website:
- **Website**: https://automationexercise.com/
- **API**: https://automationexercise.com/api/

## 📚 Dependencies

- `pytest==7.4.3` - Testing framework
- `selenium==4.15.2` - Web automation
- `requests==2.31.0` - HTTP requests
- `webdriver-manager==4.0.1` - Driver management
- `pytest-html==4.1.1` - HTML reports

## 🤝 Contributing

1. Fork project
2. Buat branch baru
3. Commit changes
4. Push ke branch
5. Buat Pull Request

## 📄 License

MIT License 