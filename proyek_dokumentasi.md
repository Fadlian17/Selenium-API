# Dokumentasi Proyek Selenium API

## 1. Detail Proyek Saat Ini
Proyek ini terdiri dari beberapa modul otomasi pengujian berbasis Selenium untuk berbagai tingkat kompleksitas (Dasar, Medium, High). Struktur folder meliputi:
- **SeleniumDriverDasar**: Contoh dasar penggunaan Selenium, script sederhana, dan laporan HTML.
- **SeleniumMedium**: Pengujian tingkat menengah, termasuk pengelolaan driver, logging, screenshot, dan laporan hasil tes.
- **SeleniumHigh**: Pengujian tingkat lanjut, API client, modular test suite, dan sistem pelaporan custom.

Fitur utama:
- Otomasi pengujian web dengan Selenium WebDriver
- Pengelolaan driver Chrome
- Laporan hasil pengujian (HTML)
- Logging dan screenshot error
- Struktur modular untuk pengujian API dan UI

## 2. Rencana Pengembangan Kedepan
- Integrasi CI/CD untuk otomatisasi pengujian
- Penambahan pengujian API yang lebih komprehensif
- Peningkatan sistem pelaporan (PDF, email notifikasi)
- Dokumentasi dan panduan penggunaan lebih detail
- Penambahan test coverage untuk skenario edge case

## 3. Panduan QA
- QA dapat menjalankan script pengujian di folder `tests/` pada masing-masing modul
- Laporan hasil pengujian dapat ditemukan di folder `reports/`
- Untuk debugging, cek folder `logs/` dan `screenshots/`
- Driver Chrome sudah disediakan di folder `drivers/`
- Untuk pengujian API, gunakan script di folder `scripts/` dan `api/`

Jika ada kendala, cek file README.md di masing-masing modul untuk instruksi lebih lanjut.
