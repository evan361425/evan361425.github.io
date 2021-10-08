# Vault PKI

公開金鑰基礎建設 Public Key Infrastructure

## 傳統流程

1. 建立 Certificate Signing Request (CSR)
   - 自己產生公私鑰
   - 用私鑰簽署 CSR
2. 寄發 CSR 給 Certificate Authority (CA)
3. CA 簽署該 CSR
   - 回傳的東西就是你的 Certificate
4. 若撤銷 CSR 則可能
   - 更新 CA 本地端的 Certificate Revocation List (CRL)
   - 或線上的 Online Certificate Status Protocal (OCSP)

## 有 Vault 的流程

### 若 root CA 放在 Vault 外面

1. 建立 root CA 在 Vault 外面
2. 建立 intermediate CA 在 Vault 裡面
3. 建立 intermediate CA 的 CSR
4. 拿出 CSR 並給 root CA 簽署後放進 Vault 裡面

### 若 root CA 在 Vault 裡面

順著上述流程打 API 就好
Vault 會幫我們做好各種溝通

## 撤銷

- 短期的 TTL 可以省掉撤銷的機制，並且縮短 CRL 的長度
- 不建議利用 command 撤銷，多利用短期的 TTL 和自動化去達到安全性

## Demo

### 環境

```bash
$ vault secrets enable -path=root-pki pki
```

### 建立 root CA

```bash
$ vault write root-pki/root/generate/internal \
  common_name="My Root CA" \
  ttl=24h

# issuing certificate, CRL distribution points, and OCSP server endpoints
$ vault write root-pki/config/urls \
  issuing_certificates="$VAULT_ADDR/v1/root-pki/ca" \
  crl_distribution_points="$VAULT_ADDR/v1/root-pki/crl"

# See configuration
$ curl -s "$VAULT_ADDR/v1/root-pki/ca/pem" | openssl x509 -text
```

> `/ca/pem` 無法透過 CLI 獲得，且不需驗證即可得到該值。
> [相關說明](https://www.vaultproject.io/api-docs/secret/pki#read-ca-certificate)

```
-----BEGIN CERTIFICATE-----
MIIDITCCAgmgAwIBAgIUB+EbBBHSHVRn+onGcck9Fq8MI0EwDQYJKoZIhvcNAQEL
BQAwGDEWMBQGA1UEAxMNVmF1bHQgUm9vdCBDQTAeFw0yMTA3MjYwODQ4NDNaFw0y
MTA3MjYwOTQ5MTJaMBgxFjAUBgNVBAMTDVZhdWx0IFJvb3QgQ0EwggEiMA0GCSqG
SIb3DQEBAQUAA4IBDwAwggEKAoIBAQCtIl1caDwF/H4TiB7PwGRvc3FrSZfp0A5A
jPOGkcP8x0aNDz+RV+WVya2ANNXou4rIICWJDhkfUTNXkDXVCOcxeCl6x211EP69
6BkyGvbf7bIhMVcMmrzNqoHWSBFdPT0/rztdlUTgmW0ukYEdfSghrsGsaaAbxyyE
aze+5dESuFQv+RXWp34kX81UJt+Z3e39DrjBWPDCoJUM6g6IijRgy0vVdV05GHmS
SKGPqf03/2Iw9xmDEui4iomclqwvmG07UivEdD1pb4nZJBmCLnWXTe/5a9+1QdQf
7xEFAMpXOqHG9EQJWzG3rjNb5MhR+VXytNDq6nteEbaaiQwB6KhXAgMBAAGjYzBh
MA4GA1UdDwEB/wQEAwIBBjAPBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQWBBTCy+Pz
4mqP6gnIkXkeq88JW4ExFDAfBgNVHSMEGDAWgBTCy+Pz4mqP6gnIkXkeq88JW4Ex
FDANBgkqhkiG9w0BAQsFAAOCAQEADdzNcD085699P/cB24JKFk49zidHe33NwEI0
7Y9tPaAChPc6ZDOUX1wguy2QL8NpZNKbxAU73HXFKHK1UOGgJQxzOUKdGLRAKc5z
E7pUF1lAyG2caJ4XtuECXKcFI/m2oaI5v+Mj8eeEv0PqV5aOmKqBsJfDtepZRYdj
0wzV8gyag2Y9rLMeveUmWF73y2l6g7KspSF0YXqzjZTJQj5oQcAmvdxSmKB8UBYD
1Rpa5Wdoq/XMwFPxL3b3qFuK+seGZzwvY9WGey5kAZQBZkkkWw519ZFGdiU1/Xjm
L4zS/WOwyBRamvriYB2fG09Vtr+i+tGsghgzEm1smu0uSSPNhA==
-----END CERTIFICATE-----%
```

### 建立 intermediate CA

```bash
$ vault secrets enable -path=int-pki pki
$ vault write -field=csr \
  int-pki/intermediate/generate/internal \
  common_name="My Intermediate CA" \
  ttl=12h > cert/intermediate.csr

# Get signed CSR from root
$ vault write -field=certificate \
  root-pki/root/sign-intermediate \
  csr=@cert/intermediate.csr \
  format=pem_bundle \
  ttl=12h > cert/intermediate.crt

# Root CA sign intermediate
$ vault write int-pki/intermediate/set-signed \
  certificate=@cert/intermediate.crt

# Urls
$ vault write int-pki/config/urls \
  issuing_certificates="$VAULT_ADDR/v1/int-pki/ca" \
  crl_distribution_points="$VAULT_ADDR/v1/int-pki/crl"

# Set role
$ vault write int-pki/roles/example-dot-com \
  allowed_domains=example.com \
  allow_subdomains=true \
  allow_glob_domains=true \
  generate_lease=true \
  max_ttl=1m \
  ttl=1m
```

> 上述建立的 public url 可透過 `curl $VAULT_ADDR/vi/int-pki/ca/pem`，以 PEM 格式取得。

取得的 CA，可以看到有效期限是 12 小時：

```
Common Name: My Intermediate CA
Issuing Certificate: My Root CA
Serial Number: 2EEF1ACC06016AE04CE00FE575D7426CEE982582
Signature: sha256WithRSAEncryption
Valid From: 07:16:44 21 Jul 2021
Valid To: 19:17:14 21 Jul 2021
Key Usage: Certificate Sign, CRL Sign
Basic Constraints: CA:TRUE
Subject Key Identifier: 46:C4:1E:F3:5B:EE:3D:64:88:37:CF:67:A8:E5:11:82:B5:CE:F0:18
Authority Key Identifier: keyid:71:37:14:BE:9B:66:E7:93:3E:4A:45:F1:B3:78:6E:37:30:38:CC:4D
Authority Info Access: CA Issuers - URI:http://localhost:8200/v1/root-pki/ca
```

取得的 CRL，待會 revoke certificate 之後可以看其變化：

```
Version: 2
IssuerDN: CN=My Intermediate CA
This update: Wed Jul 21 07:17:31 UTC 2021
Next update: Sat Jul 24 07:17:31 UTC 2021
Signature Algorithm: SHA256WITHRSA
Signature: 282359565d73c1ab950771e685ec352827967bd0
           a969e57cbacad44d2c435d4478de6f6139ef8594
           59fd862df7f61894f79cd1e775104ef45da7a95f
           7749ee639fda5a0e12a7a7b211d875aaf1c6a876
           7e5089492d38bd0098c4adc3d57d51fa7f5a90e6
           4ae2fd715376b65cd58a004002002b8d91a0251d
           1f01d0bdcead7784d5b55a7ce010a1830452bbd1
           2b37f62e3d85bc62c8f05111c8cbbfdc554f27ff
           588cc2efa77cd462d02a0026dc19fc5fd64b3021
           cf6bf17279e9b1ab1f13a03e3737dbe60601828f
           1e3cc669b508837b602abb9dcb221ae05047a7d4
           22859538c78eb44887cef9cdd62adf45abc8f278
           dad4dada9835ef6eccbe3a7ccd1a915b
Extensions: critical(false) 2.5.29.35 value = Sequence Tagged [0] IMPLICIT DER Octet String[20]
```

### 建立 Token

#### Policy

policy.hcl

```hcl
# Intermediate CA issue you!
path "int-pki/issue/example-dot-com" {
  "capabilities" = ["create", "update"]
}

# Root CA verify cert!
path "root-pki/cert/ca" {
  "capabilities" = ["read"]
}

# Token
path "auth/token/renew" {
  "capabilities" = ["update"]
}
path "auth/token/renew-self" {
  "capabilities" = ["update"]
}
```

#### 設定 policy 和建立 token

```bash
# Policy
$ vault policy write intermediate-pki policy.hcl
# Token
$ vault token create \
  -field=token \
  -policy=intermediate-pki \
  -ttl=1h > pki.token
```

### 利用 consul-template 去自動要 certificate

#### Template

certificate.tpl

```tpl
{{- with secret "int-pki/issue/example-dot-com" "common_name=blah.example.com" -}}
{{ .Data.certificate }}{{ end }}
```

key.tpl

```tpl
{{- with secret "int-pki/issue/example-dot-com" "common_name=blah.example.com" -}}
{{ .Data.private_key }}{{ end }}
```

#### consul-template 的參數

config.hcl

```hcl
vault {
  address = "http://127.0.0.1:8200"
  vault_agent_token_file = "pki.token"
  renew_token = true

  retry {
    attempts = 1
    backoff = "250ms"
  }
}

// log_level = "debug"

template {
  source      = "certificate.tpl"
  destination = "client.crt"
  command     = "echo generate certificate!"
}

template {
  source      = "key.tpl"
  destination = "client.key"
  command     = "echo generate key!"
}
```

#### 跑跑看吧！

```bash
$ consul-template -config=config.hcl
```

就會看到下列訊息反覆出現：

```
generate certificate!
generate key!
expiration: revoked lease: lease_id=int-pki/issue/example-dot-com/..
```

拿到的 Certificate：

```
Common Name: blah.example.com
Issuing Certificate: My Intermediate CA
Serial Number: 6C24455D423496C85411FF857EAC28127DF16B4D
Signature: sha256WithRSAEncryption
Valid From: 07:38:44 21 Jul 2021
Valid To: 07:40:14 21 Jul 2021
Key Usage: Digital Signature, Key Encipherment, Key Agreement
Extended Key Usage: TLS Web Server Authentication, TLS Web Client Authentication
Subject Key Identifier: 77:79:22:4B:12:19:5D:F2:55:FF:76:11:CE:5D:34:1C:60:4C:44:76
Authority Key Identifier: keyid:46:C4:1E:F3:5B:EE:3D:64:88:37:CF:67:A8:E5:11:82:B5:CE:F0:18
Authority Info Access: CA Issuers - URI:http://localhost:8200/v1/int-pki/ca
Subject Alternative Names: DNS:blah.example.com
```

### clean up

若要清除過期的 cert，請呼叫

```bash
$ vault write root-pki/tidy tidy_revoked_certs=true
```

> [相關說明](https://www.vaultproject.io/api-docs/secret/pki#tidy)
