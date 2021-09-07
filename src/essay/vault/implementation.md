# Vault 實作

## Server 設定

```json=
{
  "storage": {
    "mysql": {
      "address": "127.0.0.1:3306",
      "database": "playground",
      "table": "vault",
      "username": "root",
      "password": "mysql-password",
      "plaintext_connection_allowed": true,
      "ha_enabled": true
    }
  },
  "listener": {
    "tcp": {
      "tls_disable": true
    }
  },
  "seal": {
    "awskms": {
      "region": "ap-northeast-1",
      "access_key": "aws-iam-access-key",
      "secret_key": "aws-iam-secret-key",
      "kms_key_id": "aws-kms-key-id"
    }
  },
  "ui": true,
  "disable_mlock": true,
  "api_addr": "http://127.0.0.1:8200",
  "cluster_addr": "https://127.0.0.1:8201"
}
```

```bash=
$ vault server -config=config.json
```

## Seal/Unseal

初始化並獲得 `Recovery Key` 和 `Root Token`

```bash=
$ vault operator init -recovery-shares=1 -recovery-threshold=1

Recovery Key 1: fFtAyv+N/h4YdgQmLveOleONswIYmNorw6E65Jv7ciU=
Initial Root Token: s.9gFtHEu35b4FCBHbUtaLxeOw
```

```bash=
$ vault status

Key                    Value
---                    -----
Recovery Seal Type     shamir
Initialized            true
Sealed                 false
Total Recovery Shares  1
Threshold              1
Version                1.6.1
Storage Type           mysql
Cluster Name           vault-cluster-d4a98a31
Cluster ID             06bbee1f-d643-31c1-a87b-ba43d3b1d2d3
HA Enabled             true
HA Cluster             https://127.0.0.1:8201
HA Mode                active
```

### MySQL

可以看到主鑰和加密金曜都已經建立好了

```
vault_key     vault_value
---------     -----------
core/keyring  ...
core/master   ...
```

### Login

```bash=
$ vault login s.9gFtHEu35b4FCBHbUtaLxeOw
```

### Seal

重新封印並再解封的話要輸入 `Recovery Key`

> 注意：若重新申請一個 `Root Token`，也會需要 `Recovery Key`

```bash=
$ vault operator seal
$ vault operator unseal

Unseal Key (will be hidden):
```

## Secrets

key-value 的資料庫

```bash=
$ vault secrets enable -path=secret kv
$ vault kv put secret/hello foo=world
$ vault kv list secret
$ vault kv get secret/hello
```

### MySQL

可以看到資料庫依此建立了新的路徑，`secret/hello` 中的 `secret` 被加密了

```
vault_key                                           vault_value
---------                                           -----------
logical/beefac89-6bc8-6bfd-1af8-c1436c19926c/hello  ...
```

## Authentication

先允許 GitHub 登入

```bash=
$ vault auth enable github
$ vault write auth/github/config organization=104corp
```

### 登出

```bash=
$ rm ~/.vault-token
```

### GitHub

#### 存取權杖

去 [GitHub 設定頁](https://github.com/settings/profile) > Developer settings > Personal access tokens > Generate new token

權限要有：`admin:org > read:org`，讓 Vault 可以讀取你帳號的組織

#### 登入

```bash=
$ vault login -method=github -token=access-token-from-github

Key                  Value
---                  ------
token                s.AtDndppL6auMYfI27zfkvgn1
token_accessor       WC8tFkMglS9S3RLtitHdAtRe
token_duration       768h
token_renewable      true
token_policies       ["default"]
identity_policies    []
policies             ["default"]
token_meta_username  evan361425
token_meta_org       104corp
```

#### 資訊

```bash=
$ vault token lookup s.AtDndppL6auMYfI27zfkvgn1

Key                 Value
---                 -----
accessor            WC8tFkMglS9S3RLtitHdAtRe
creation_time       1610344081
creation_ttl        768h
display_name        github-evan361425
entity_id           7b404dd3-5b23-da3f-663c-76a66e84ebe8
expire_time         2021-02-12T13:48:01.492935+08:00
explicit_max_ttl    0s
id                  s.AtDndppL6auMYfI27zfkvgn1
issue_time          2021-01-11T13:48:01.492956+08:00
meta                map[org:104corp username:evan361425]
num_uses            0
orphan              true
path                auth/github/login
policies            [default]
renewable           true
ttl                 767h36m19s
type                service
```

## Token

先重新登入回 `Root Token`

```bash=
# 看看現在是用什麼權杖
$ vault print token
s.AtDndppL6auMYfI27zfkvgn1
# 此權杖並非 Root Token，登出
$ rm ~/.vault-token
$ vault login s.9gFtHEu35b4FCBHbUtaLxeOw
```

### 列出所有 token 的 accessor

```bash=
$ vault list auth/token/accessors
```

### Batch Token

先建立 [Policy](#Policy)

```bash=
$ vault token create -type=batch -orphan=true -policy=my-policy

Key                  Value
---                  -----
token                b.AAAAAQKn0sVCMJNVTBWHXpwjQ1HbgpyDsJ8WeKtVaZiiUCLK13uT4-pknd0lsHyiXVw7jaRy2U03o0K-TjtEU40v5f26KZXiY12vlMakT1WZuL-NdQ6pGD9fj4YGRp39qKY_jbQyrx8
token_accessor       n/a
token_duration       768h
token_renewable      false
token_policies       ["default" "my-policy"]
identity_policies    []
policies             ["default" "my-policy"]
```

batch token 開頭是 `b`，反之，常見的 token 是 `s` 開頭，代表 service token

### Wrapping Token

```bash=
$ vault token create -policy=my-policy -wrap-ttl=120

Key                              Value
---                              -----
wrapping_token:                  s.F7S12zD0PUcEL5VShhElBZIb
wrapping_accessor:               LsfBV3JiC4zwWCaFEZqNW9db
wrapping_token_ttl:              2m
wrapping_token_creation_time:    2021-01-11 16:49:11.614054 +0800 CST
wrapping_token_creation_path:    auth/token/create
wrapped_accessor:                oW7NNQUM35G7mvTQ4vieDPqi
```

```bash=
vault unwrap s.F7S12zD0PUcEL5VShhElBZIb

Key                  Value
---                  -----
token                s.v8lwNg4uwfZzlHvDrmPdkRyF
token_accessor       oW7NNQUM35G7mvTQ4vieDPqi
token_duration       768h
token_renewable      true
token_policies       ["default" "my-policy"]
identity_policies    []
policies             ["default" "my-policy"]
```

#### API

```bash=
$ curl \
    --header "X-Vault-Token: s.9gFtHEu35b4FCBHbUtaLxeOw" \
    --header "X-Vault-Wrap-TTL: 60" \
    --request POST \
    --data "{\"foo\": \"bar\"}" \
    http://127.0.0.1:8200/v1/sys/wrapping/wrap
{
  "request_id": "",
  "lease_id": "",
  "renewable": false,
  "lease_duration": 0,
  "data": null,
  "wrap_info": {
    "token": "s.3MeMoyxudk19RHKzCZAa55oi",
    "accessor": "6rKApXj7R8iNz3gZjkIpd8Y4",
    "ttl": 60,
    "creation_time": "2021-01-11T17:08:44.876296+08:00",
    "creation_path": "sys/wrapping/wrap"
  },
  "warnings": null,
  "auth": null
}
```

---

```bash=
$ curl \
    --header "X-Vault-Token: s.9gFtHEu35b4FCBHbUtaLxeOw" \
    --request POST \
    --data "{\"token\":\"s.3MeMoyxudk19RHKzCZAa55oi\"}" \
    http://127.0.0.1:8200/v1/sys/wrapping/lookup
{
  "request_id": "67be1f69-e921-0eac-a660-5aa4f2761cb1",
  "lease_id": "",
  "renewable": false,
  "lease_duration": 0,
  "data": {
    "creation_path": "sys/wrapping/wrap",
    "creation_time": "2021-01-11T17:11:00.784059+08:00",
    "creation_ttl": 60
  },
  "wrap_info": null,
  "warnings": null,
  "auth": null
}
```

## Policy

### 讀取現有的政策

```bash=
$ vault read sys/policy

Key         Value
---         -----
keys        [default root]
policies    [default root]
```

### 建立政策

```bash=
$ vault policy write my-policy policy.hcl
```

`policy.hcl` 檔：

```hcl
path "secret/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

path "secret/hello" {
  capabilities = ["deny"]
}

path "secret/restricted" {
  capabilities = ["create"]
  allowed_parameters = {
    "foo" = []
    "bar" = ["zip", "zap"]
  }
}
```

## High Availability

Different from [config](#Server-設定)

```json=
{
  "listener": {
    "tcp": {
      "address": "127.0.0.1:8100",
      "cluster_address": "127.0.0.1:8101"
    }
  }
}
```

```bash=
$ export VAULT_ADDR="http://127.0.0.1:8100"
$ vault status

Key                      Value
---                      -----
Recovery Seal Type       shamir
Initialized              true
Sealed                   false
Total Recovery Shares    1
Threshold                1
Version                  1.6.1
Storage Type             mysql
Cluster Name             vault-cluster-d4a98a31
Cluster ID               06bbee1f-d643-31c1-a87b-ba43d3b1d2d3
HA Enabled               true
HA Cluster               https://127.0.0.1:8201
HA Mode                  standby
Active Node Address      http://127.0.0.1:8200
```

## Rate Limit

```bash=
$ vault read sys/quotas/config

Key                                   Value
---                                   -----
enable_rate_limit_audit_logging       false
enable_rate_limit_response_headers    false
rate_limit_exempt_paths               [
                                        /v1/sys/generate-recovery-token/attempt
                                        /v1/sys/generate-recovery-token/update
                                        /v1/sys/generate-root/attempt
                                        /v1/sys/generate-root/update
                                        /v1/sys/health
                                        /v1/sys/seal-status
                                        /v1/sys/unseal
                                      ]
```

### 存取、編輯

```bash=
$ vault write sys/quotas/rate-limit/global-rate rate=500
$ vault read sys/quotas/rate-limit/global-rate

Key               Value
---               -----
block_interval    0
interval          1
name              global-rate
path              n/a
rate              500
type              rate-limit
```

```bash=
$ vault write sys/quotas/rate-limit/global-rate rate=501
$ vault delete sys/quotas/rate-limit/global-rate
```

## Debug

```bash=
$ vault debug
```
