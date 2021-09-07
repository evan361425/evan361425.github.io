# Vault Transit

## 功能

讓 Vault 變成一台幫忙處理加解密的機器

- 明文輸入，密文輸出。
- 密文輸入，透過密文的字首判斷是哪一個金鑰做的加密，輸出明文。
- 也可以純做簽、驗證。

## 金鑰轉換

- 會把該版本的金鑰所產生的密文加上該版本的標頭。
  - v1 key encryption result: `vault:v1:8SDd3WHDO...`
  - v5 key encryption result: `vault:v5:bXkgc2Vjc...`
- 可以在透過參數 `min_decryption_version` 禁止使用過舊的金鑰。
- 若轉換過多金鑰會造成效率問題
  - 可以產生全新的金鑰來避免過大的鑰匙版本
  - `key1:v8:abc...` => post to `key1` with `vault:v8:abc...`
  - `key2:v6:def...` => post to `key2` with `vault:v6:def...`

## 金鑰版本限制

- `min_decryption_version`, `min_encryption_version`, `min_available_version`（刪除舊版本的金鑰）
- 如果要逐步淘汰舊版的金鑰呢？
- rewrap - 把指定的密文解密並重新用新的金鑰加密
  - `key_version` - 預設為最新版的金鑰
  - `batch_input`

## 特殊功能

### Key derivation

- 加解密會需要 `content`（和 `salt` 一樣）。
- `new key = HMAC(key, content)`
- 讓鑰匙在每次加密都不一樣，擁有更高的安全性。

### Convergent encryption

- 確保當明文一樣，密文就會一樣。
- 用途之一：可以避免重複的資料存入 DB
- 必須配合使用 key derivation 保證安全性。
- 輸入明文外還要輸入 `nonce`。

### Datakey generation

- 用途之一：加密大量資料，避免頻寬的佔用。
- 產生鑰匙。
- 利用加解密金鑰加密此鑰匙。
  1. 輸出加密後的鑰匙
     - 重新要求解密得到真正的鑰匙
  2. 直接輸出真正的鑰匙
  3. 預設：兩個都輸出

## DEMO

### 環境

```bash=
$ vault secrets enable transit
# -f for force post request when no data
$ vault write -f transit/keys/example
$ vault policy write transit-example policy.hcl
$ vault token create \
  -field=token \
  -policy=transit-example \
  -ttl=1h
```

### 加密

```bash=
$ vault write -field=ciphertext \
  transit/encrypt/example \
  plaintext=$(base64 <<< "4111 1111 1111 1111")

vault:v1:+W+aOV4DqhOLqCmTZ2oRqj6qAjTyZNYkoYfUraPl88XwEy3hC8Ul2WyrcP8Mz/sg
```

### 解密

```bash=
$ vault write -field=plaintext \
  transit/decrypt/example \
  ciphertext='vault:v1:+W+aOV4DqhOLqCmTZ2oRqj6qAjTyZNYkoYfUraPl88XwEy3hC8Ul2WyrcP8Mz/sg'

NDExMSAxMTExIDExMTEgMTExMQo=
```

### 金鑰轉換

```bash=
$ vault write -f transit/keys/example/rotate
$ vault write -field=ciphertext \
  transit/encrypt/example \
  plaintext=$(base64 <<< "4111 1111 1111 1111")

vault:v2:Dbpgk1UhlY+74uj8ecmFEiYfriDTWZc907VgO1EWfSXmMnPW3j+qDaetDlnOTVOI
```

### 金鑰限制

```bash=
$ vault write transit/keys/example/config \
  min_decryption_version=2 \
  min_encryption_version=2

# Decrypt v1 will return error
$ vault write transit/decrypt/example \
  ciphertext='vault:v1:+W+aOV4DqhOLqCmTZ2oRqj6qAjTyZNYkoYfUraPl88XwEy3hC8Ul2WyrcP8Mz/sg'
```

### 重包密文

```bash=
$ vault write transit/keys/example/config min_decryption_version=1
$ vault write -field=ciphertext \
  transit/rewrap/example \
  ciphertext='vault:v1:+W+aOV4DqhOLqCmTZ2oRqj6qAjTyZNYkoYfUraPl88XwEy3hC8Ul2WyrcP8Mz/sg'
```

### 永久刪除舊版金鑰

```bash=
$ vault write transit/keys/example/config min_decryption_version=2
$ vault write transit/keys/example/trim min_available_version=2
```

## 金鑰可以容忍的最大版本數量

| 金鑰種類             | Consul 預設值 (512 KiB) |
| -------------------- | ----------------------- |
| aes128-gcm96 keys    | 2008                    |
| aes256-gcm96 keys    | 1865                    |
| chacha-poly1305 keys | 1865                    |
| ed25519 keys         | 1420                    |
| ecdsa-p256 keys      | 817                     |
| ecdsa-p384 keys      | 659                     |
| ecdsa-p523 keys      | 539                     |
| 1024-bit RSA keys    | 169                     |
| 2048-bit RSA keys    | 116                     |
| 4096-bit RSA kyes    | 89                      |
