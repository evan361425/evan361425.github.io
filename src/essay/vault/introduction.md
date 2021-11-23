# Vault 介紹

![Vault Structure](https://i.imgur.com/ghaX92s.png)

---

## Seal/Unseal

封印/解封

```mermaid
graph LR
    subgraph g1 [解封]
    sf[加解密金鑰]
    end
    subgraph 初始化
    s1[(產生 加解密金鑰)] --> sf
    s2[輸出 解封金鑰]
    end
    subgraph 建立和資料庫的連線<br>封印
    s0[沒有金鑰] --> s1
    s0 -- 透過 解封金鑰 獲得 --> sf
    end
```

### 解封金鑰換得加解密金鑰

```mermaid
graph LR
    k1[解封金鑰] -- 解密<br>丟棄 --> k2[(加密後的主鑰匙)]
    subgraph 資料庫
    k2 -- 解密<br>記憶 --> 3[(加密後的鑰匙圈)]
    end
```

### 解封金鑰

#### Shamir Unseal Keys

-   需要多把鑰匙去組合出一把真正的解封金鑰
-   可設定所需金鑰的閥值
-   手動輸入

#### Auto Seal

-   AWSKMS, GCP Cloud KMS, OCI KMS ...
-   會產生 `recovery key`
-   透過 `recovery key` **授權** KMS 去解封 Vault
-   透過 `recovery key` 去重新設定解封參數

---

## Lease, Renew, Revoke

使用特定方式驗證或服務時時會給予`租賃`，需要使用者定期`刷新`，以避免過期。

管理方也可`撤銷`指定的`租賃`。

---

例如：動態獲得 `AWS` 的存取權杖

```bash
$ vault read aws/creds/my-role
Key             Value
---             -----
lease_id        aws/creds/my-role/f3e92392-7d9c-09c8-c921-575d62fe80d8
lease_duration  768h
lease_renewable true
access_key      AKIAIOWQXTLW36DV7IEA
secret_key      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
security_token  <nil>

```

## Authentication

驗證過後才能執行所有需要執行的動作，除了最一開始的 `init` 和 `unseal`。

### 驗證方法

GitHub, LDAP, AppRole ...

### Tokens

驗證成功會給予 token

## Tokens

權杖

-   最一開始的權杖 即是在建立之初所得到的 `Root Token`
-   透過設定，允許不同的[驗證方法](#驗證方法)，每次登入都會給予一個權杖
-   透過[政策](#Policy)去管理
-   有時候會透過權杖去取得`租賃`。

### Root Token

根權杖

-   應該在初始化操作（[驗證方法](#驗證方法)和[政策](#Policy)）後`撤銷`
-   若有需要根權杖，可透過 `vault operator generate-root` 去產生
    -   需要解封鑰匙
    -   [詳見](https://learn.hashicorp.com/tutorials/vault/generate-root)

### 權杖的制度

-   透過權杖，可以生產全新的權杖，此時該權杖稱為子權杖，若建立子權杖的權杖被撤銷，子權杖同時會被撤銷
    -   避免過大的家族導致撤銷的困難
-   仍能特過特殊方式建立沒有父母的權杖 `Orphan Token`，[詳見](https://www.vaultproject.io/docs/concepts/tokens#token-hierarchies-and-orphan-tokens)

### 權杖的 accessor

用來代表該權杖的路標，可用此路標

-   查看該權杖的資訊，除了權杖 ID 本身，[詳見](https://www.vaultproject.io/docs/commands/token/lookup#examples)
-   查看該權杖可否使用可以特定權利（僅能 API），[詳見](https://www.vaultproject.io/api-docs/system/capabilities-accessor#sys-capabilities-accessor)
-   撤銷權杖，[詳見](https://www.vaultproject.io/docs/commands/token/revoke#examples)
-   重新計算權杖的過期時間（僅限 API），[詳見](https://www.vaultproject.io/api-docs/auth/token#renew-a-token-accessor)

### 權杖的過期

-   可重新計算權杖的過期時間。並非疊加，而是重新計算
-   給予機器短時間的權杖，並要求短時間內重新計算過期時間。以確保機器存活狀態
-   給予非機器長時間（32 天）的權杖

### Batch Tokens

-   權杖中含有足夠的資訊去做事情
-   若沒有父母，可以在不同的機器（Node）間使用

```bash
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

## Response Wrapping

1. 一台機器驗證通過後得到權杖，並持續更新權杖保持其可用性。
    - 但是機器如果需要重啟？
2. 不能保證機器的合法性，但需要他獲得權杖
    - 手機 app

把權杖包裝（Wrapping）起來給指定機器。

```bash
$ vault token create -policy=apps -wrap-ttl=120
```

```mermaid
graph LR
    root -- 1. 要求包裝權杖 --> Vault
    root -- 2. 寄送包裝權杖 --> APP
    APP -- 3. 透過包裝權杖取得權杖 --> Vault
    APP -- 4. 特過權杖取得資訊 --> Vault
```

### 關於包裝權杖

-   若沒有包裝權杖仍可透過 `unwrap-accessor` 去撤銷其代表的權杖
-   包裝權杖並未做簽證（sign），因為其利用 key-value 去獲得真正的權杖，[詳見](https://www.vaultproject.io/docs/concepts/response-wrapping#response-wrapping-tokens)
-   [實作](https://hackmd.io/idIbJh-aRj-yT7_1Q5AqKQ#Wrapping-Token)

### 安全性做法

-   建立 Audit Log Device 做紀錄。
-   每次得到包裝權杖，執行 Look-up，可以得到建造其的位置，並做驗證。

## Policy

政策

-   根據驗證方式，可以設計不同單位（甚至個體）不同政策
-   通常是限制可以獲取哪些資料和對該資料的處理權限
-   `create`, `read`, `update`, `delete`, `list`
-   `sudo`, `deny`
-   可以要求指定資料必須`包裝`

---

```mermaid
graph LR
    root -- 建立驗證方式 --> Vault
    root -- 政策 --> Vault
    Vault -- 儲存 --> k[(資料庫)]
```

```mermaid
graph LR
    user -- 1. 驗證 --> Vault
    Vault -- 2. 確認 --> 驗證機構
    k[(資料庫)] -- 3. 政策 --> Vault
    Vault -- 4.權杖 --> user
```

### 注意事項

-   寫作方式，[詳見](https://www.vaultproject.io/docs/concepts/policies#policy-syntax)
-   政策模板，讓每個人僅能讀取各自的資料，[詳見](https://www.vaultproject.io/docs/concepts/policies#templated-policies)
-   限制特定 key-value 的存取，[詳見](https://www.vaultproject.io/docs/concepts/policies#parameter-constraints)
-   列表、讀取、編輯、刪除，[詳見](https://www.vaultproject.io/docs/concepts/policies#managing-policies)

## High Availability

![Relation between cluster and node](https://i.imgur.com/5diYphY.png)

-   Standby-node 只會把需求**重新導向**至 Active-node
-   Standby-node 透過**資料庫**得到 Active-node 的資訊
-   一般來說，效能瓶頸是來自於資料庫的編輯和存取
-   Performance Standby-node（付費）
    -   允許 Standby-node 讀取資料

### 重新導向

1. Standby-node 和 Active-node 溝通（預設值）
    - 透過**資料庫**的私鑰和簽章來和 Active node 做 TLS1.2 溝通
    - `cluster_address`
2. Standby-node 回應 `307` 給使用者，並要求重新導向至 Active-node
    - 若有 Load Balance 可以重新導向至此
    - `api_address`

## Integrated Storage

如果資料庫不能連線了...？

> 建立多個資料庫並整合

1. [RAFT](http://thesecretlivesofdata.com/raft) - 幫助多個資料庫的整合
2. 資料庫是用 File System
3. 每個 Node 都需要有一個獨立的資料庫，但是會和其他 Node 整合

## 計數

-   API，[詳見](https://learn.hashicorp.com/tutorials/vault/resource-quotas)
    -   可以限制其次數
-   User，[詳見](https://www.vaultproject.io/docs/concepts/client-count)
    -   獨立個體（透過特定驗證方式）+ 非獨立個體的權杖
