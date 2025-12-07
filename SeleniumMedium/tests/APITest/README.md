# Mapping Test Automation dengan API

Berikut adalah mapping antara endpoint API darihttps://thinking-tester-contact-list.herokuapp.com/ dan implementasi test automation pada folder SeleniumMedium:

| Endpoint                      | Method | Deskripsi                        | Nama File Test                |
|-------------------------------|--------|----------------------------------|-------------------------------|
| /productsList                 | GET    | Mendapatkan list produk          | test_get_products_list.py     |
| /brandsList                   | GET    | Mendapatkan list brand           | test_get_brands_list.py       |
| /searchProduct                | POST   | Mencari produk                   | test_search_product.py        |
| /login                        | POST   | Login user                       | test_login_user.py            |
| /verifyLogin                  | POST   | Verifikasi login user            | test_verify_login.py          |
| /createAccount                | POST   | Register user baru               | test_create_account.py        |
| /deleteAccount                | DELETE | Hapus user account               | test_delete_account.py        |
| /updateAccount                | PUT    | Update user account              | test_update_account.py        |
| /getUserDetailByEmail         | GET    | Mendapatkan detail user by email | test_get_user_detail.py       |

## Implementasi
- Setiap endpoint sudah dibuatkan file test terpisah di folder `tests/APITest/`.
- Setiap file test menggunakan library `requests` dan `pytest` untuk skenario positif dan negatif.
- Hasil test dapat dijalankan dengan perintah:

```bash
pytest SeleniumMedium/tests/APITest/ -v
```

- Hasil test dan error akan terdokumentasi di laporan HTML dan log.

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

Setiap file test berisi skenario positif dan negatif sesuai dokumentasi API dan koleksi Postman.
