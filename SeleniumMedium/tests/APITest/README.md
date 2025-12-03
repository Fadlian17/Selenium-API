# Mapping Test Automation dengan API

Berikut adalah mapping antara endpoint API dari https://automationexercise.com/api_list dan rencana implementasi test automation pada folder SeleniumMedium:

| Endpoint                      | Method | Deskripsi                        | Nama Test                |
|-------------------------------|--------|----------------------------------|--------------------------|
| /productsList                 | GET    | Mendapatkan list produk          | test_get_products_list   |
| /brandsList                   | GET    | Mendapatkan list brand           | test_get_brands_list     |
| /searchProduct                | POST   | Mencari produk                   | test_search_product      |
| /login                        | POST   | Login user                       | test_login_user          |
| /verifyLogin                  | POST   | Verifikasi login user            | test_verify_login        |
| /createAccount                | POST   | Register user baru               | test_create_account      |
| /deleteAccount                | DELETE | Hapus user account               | test_delete_account      |
| /updateAccount                | PUT    | Update user account              | test_update_account      |
| /getUserDetailByEmail         | GET    | Mendapatkan detail user by email | test_get_user_detail     |

## Rencana Implementasi
- Setiap endpoint akan dibuatkan file test terpisah di folder `tests/APITest/`.
- Setiap file test akan menggunakan requests dan assertion sesuai response yang diharapkan.
- Hasil test akan dilog dan didokumentasikan di laporan HTML.

Contoh struktur folder:
```
SeleniumMedium/
  tests/
    APITest/
      test_get_products_list.py
      test_get_brands_list.py
      test_search_product.py
      test_login_user.py
      test_verify_login.py
      test_create_account.py
      test_delete_account.py
      test_update_account.py
      test_get_user_detail.py
```

Setiap file test akan berisi skenario positif dan negatif sesuai dokumentasi API.
