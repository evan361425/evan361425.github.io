# 建置 PKI 注意事項

本資料來源於 [NIST 800-32 Ct.3](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-32.pdf)

-   [Certification Path Building](https://www.rfc-editor.org/rfc/rfc4158.html#page-14)
-   [Key Rollover in the Resource Public Key Infrastructure](https://datatracker.ietf.org/doc/html/rfc6489)
-   [X.509](https://datatracker.ietf.org/doc/html/rfc5280#section-6.1)

```

 ┌─────────────────────────────────────────────┐
 │                   IDC                       │
 │                      ┌────────┐             │
 │                      │  Root  │             │
 │                      └────▲───┘             │
 │                           │                 │
 │                      HTTP │                 │
 │                           │                 │
 │      HTTP          ┌──────▼─────┐           │
 │  ┌─────────────────►            │           │
 │  │                 │Intermediate│           │
 │  │            ┌────►            ◄────┐      │
 │  │       HTTP │    └──────▲─────┘    │      │
 │  │            │           │          │      │
 │  │         ┌──▼───┐     ┌─▼────┐   ┌─▼────┐ │
 │  │      ┌──► AES  ◄───┐ │  EE  │   │  EE  │ │
 │  │      │  └─▲────┘   │ └──────┘   └──────┘ │
 │  │ HTTPS│    │        │                     │
 │  │      │    └────┐   └─────┐               │
 │  │      │         │         │               │
 │  │   ┌──┴──┐ ┌────┴────┐ ┌──┴──┐            │
 │  └───┤ API │ │ Service │ │ APP │            │
 │      └─────┘ └─────────┘ └─────┘            │
 │                                             │
 └─────────────────────────────────────────────┘
```

可能需要溝通的原因：

-   初始註冊/認證
-   金鑰對更新
-   憑證更新

## NIST

### 名詞介紹

-   CA 簽署簽證給 user，此時 CA 是 issuer。
-   CA 會把驗證 user 的資訊丟給 Registration Authority(RA)，例如：DNS
-   使用 CA 簽出來的簽證，並以此來信任 user 的第三方稱為 relying parties

_certificate policy_ 定義簽證的政策，例如該用什麼金鑰種類、長度。能做到檢查的步驟，實務上僅有簽發時作檢查，然後再把資訊放在簽證上。

> correctly configuring root certificate stores is a critical step in key management.

**X.509** 會放

-   user name
-   issuer name
-   public key
-   signature
-   validity (starting and expiring times)
-   cryptographic algorithm(s)
-   和其他 Private 的 extension

驗證過程

-   Cross certificates，就算是 root CA(_trust anchors_)也可能會需要其他同樣是 root CA 的簽證。
-   certification path，relying party 從 user 到 trust anchors 的驗證流程

驗證過程中的每一段都需要確認（path validation）：

-   簽證驗證
-   簽證沒被撤銷
-   被正確的政策 issue

簽證的狀態展示（簽證沒被撤銷）方式有兩種：

-   Online Certificate Status Protocol (OCSP)
-   certificate revocation list, or CRL

若一開始是使用 **key establishment** 做簽證，要可以做金鑰的回復。

### Procurement Guidance

挑選 CA 產品的 check list。

#### CA/RA Software and Hardware:

-   [ ] 確保支援任一協定：
    -   Certificate Management Protocol (CMP) [RFC 4210](https://datatracker.ietf.org/doc/html/rfc4210)
    -   Enrollment over Secure Transport (EST) [RFC 7030](https://datatracker.ietf.org/doc/html/rfc7030)
    -   Certificate Management Using Cryptographic Message Syntax (CMC) [RFC 5272](https://datatracker.ietf.org/doc/html/rfc5272)
-   [ ] 確保可以產生憑證，其中應含有的資訊於後討論之。
-   [ ] 可以產生多組憑證，且允許特定金鑰種類。
-   [ ] 允許 CRL。
-   [ ] 允許外部連結 CRL，且必須含有 HTTP URLS。
-   [ ] 應可以透過 LDPA 取得 CRL。
-   [ ] 允許 OCSP。
-   [ ] 每組 PKI 都有其憑證資訊，且資訊能被顯示於其簽署的簽證 CRL。
-   [ ] 允許設定客制相關資訊於憑證中。
-   [ ] 允許使用 RSA 和 ECDSA 演算法。
-   [ ] 可以備份並災難復原。
-   [ ] 允許權限在帳號之間的轉移。

#### OCSP Responders:

-   [ ] 確保 OCSP responders 符合 [RFC 6960](https://datatracker.ietf.org/doc/html/rfc6960) _Online Certificate Status Protocol_。
-   [ ] 確保能處理有無簽章和名稱的請求，就算是拒絕也須回應。
-   [ ] 回應時沒有任何於 [RFC 5019](https://datatracker.ietf.org/doc/html/rfc5019) 中提及的錯誤
-   [ ] 回應時的簽章建議符合和其產生的憑證的演算法相同，金鑰格式也建議一樣。允許使用 RSA 和 ECDSA 演算法。

#### 加密模組

-   [ ] CAs、Key Recovery Servers 和 OCSP responders 高於 [FIPS 140-2](https://csrc.nist.gov/publications/detail/fips/140/2/final) 等級 3。
-   [ ] RAs 需高於 FIPS 140-2 等級 2。
-   [ ] 確保請求簽證的單位和使用者的加密模組高於 FIPS 140-2 等級 1。

#### Key Recovery Servers

-   [ ] 如果 PKI 支援金鑰產生，就應支援金鑰救援服務。
-   [ ] 應支援自動化的金鑰救援服務。

#### Relying Party Software

-   [ ] 路程驗證（path validation）
    -   [ ] 確保符合 [RFC 5280](https://datatracker.ietf.org/doc/html/rfc5280) _conformant path validation_。
    -   [ ] 允許組織外的驗證（例如透過 federal agency）且需符合 [NIST 建議的驗證方式](https://csrc.nist.gov/projects/pki-testing/)。
    -   [ ] 允許有 Bridge 的路徑，且需符合 [NIST 建議的驗證方式](https://csrc.nist.gov/projects/pki-testing/)。
    -   [ ] 應該同時支援 CRLs 和 OCSP。
-   驗證憑證
    -   [ ] 確保可以建立驗證的路徑
    -   [ ] 至少要能處理 HTTP-based 的回應
    -   [ ] 應要能處理 LDAP 的協定
-   [ ] 作用於企業端 PKI 的 RP 應能發現路徑上受 trust anchor CA 認證的階層式 CA。
-   [ ] 非企業端 PKI 的 RP 應能發現路徑上非階層式的 CA。

#### Client Software

-   [ ] 客戶端允許多個公私鑰請求多個簽證
-   [ ] 加密模組高於 FIPS 140-2 等級 1
-   [ ] 客戶應可使用 CA 提供的 certificate management protocol

### 給 PKI 管理者的建議

管理者應確保使用端的人接受必要訓練和公司安全政策被執行。

#### Certificate Issuance

-   [ ] 確保 CAs 設定好可接受的公私鑰演算法和金鑰長度，還有驗證 domain
-   [ ] 為了最大化標準性，應使用 RSA 去做簽章和金鑰轉移
-   [ ] 為了最大化安全性和效率，應使用 EC 去做簽章和金鑰轉移
-   [ ] 當簽發簽證或 CRLs 時，應符合演算法、長度的規範
-   [ ] 利用 subject key 產生 signing key 時，簽證的安全性應大於 subject key 去簽證
-   產生金鑰時：
    -   [ ] 使用者應產生屬於他們自己的簽證金鑰
    -   [ ] 若上 PKI 透過金鑰傳送方式去傳送金鑰，應提供金鑰復原服務
    -   [ ] CAs 要確保金鑰真的屬於使用者（PoP）
-   [ ] 應在簽證前先驗證金鑰
-   Key usage extension
    -   [ ] 簽證應包含 key-ussage extension
    -   [ ] key-ussage extension 應限制一種獲取方式，使用者自己產生或 PKI 產生
-   [ ] 所有簽證應包含 CRLs 的位置資訊
-   [ ] 若提供 OCSP responder，應提供位置資訊於簽證中
-   [ ] 在過期前應重新簽署完成，並且正確更新憑證資訊，如 domain 或信箱

#### Certificate Revocation Requests

-   [ ] 應提供自動撤銷機制：
    -   [ ] CAs 應在撤銷時進行身份驗證
    -   [ ] 使用者提供身份證明並要求撤銷時，應在不需人力介入下執行。
-   [ ] RAs 應能在設定後，代表使用者或公司請求簽證撤銷

#### Certificate Revocation List Generation

-   [ ] 為了最大標準化，CAs 應提供完整的撤銷簽證於 CRL 中
-   [ ] 若有大量的撤銷簽證，可以產生部分的 CRL，但須額外提供完整的 CRL 位置資訊。一份 CRL 不應超過 250,000 的撤銷簽證。

#### PKI Repositories for the Distribution of Certificates and CRLs

-   [ ] PKIs 應能公開提供簽證和 CRL
-   [ ] PKI 庫應能提供身份驗證後的簽證位置修改和 PKI 庫的 CRL 分佈
-   [ ] PKI 庫應至少允許 HTTP 1.1 或 LDAP version 3
-   [ ] 為了最大標準化， HTTP 和 LDAP 都應被符合
-   [ ] HA 應被考慮
-   [ ] PKI 庫應包含所有其擁有的 PKI 的所有簽證
-   [ ] PKI 庫應包含所有其擁有的 PKI 的 CRL

#### OCSP Responders

For federal agencies, detailed configuration guidance for OCSP responders is specified in Draft Guidance for OCSP Responders in the U.S. Federal PKI.17

-   為了最大標準化：
    -   [ ] OCSP responders 不應要求請求要有簽名，且不能限制哪些簽證狀態是可以被允許的
    -   [ ] 應能回應基本的資訊，且不能含有危險的 extensions
-   若僅需符合內部社群而非標準化：
    -   [ ] OCSP responders 可要求請求要有簽名，且可拒絕外部的請求
    -   [ ] OCSP 的回應訊息可能含有特殊的 extensions

#### Backup and Archive

-   [ ] 應該備份資料，並當災難發生後能重新啟用
-   [ ] CAs 應紀錄何時和何人申請的簽證
-   [ ] 應有 log 紀錄所有簽證和 CRL
-   [ ] 申請人的公鑰應和其簽證一起被保存

#### Relying Party Integration and Configuration

-   [ ] 應可以發現路徑和獲得狀態資訊
-   [ ] 應要可以支援 CRL 和 OCSP 的格式
-   [ ] 應能分辨最小單位的 trust anchors
-   [ ] 當情境處於「公司對政府」或「政府對政府」，應使用 Common Policy Root CA 或和 Common Policy Root CA 互相認證的 CA 或以 Federal Bridge 為 trust anchor 的 CA
-   [ ] 當情境屬於「使用者對政府」，應用程式的安全性無法做到高度限制，為了達成高標準性，使用者可能會使用的預先安裝至 COTS products 的 trust anchors
-   路徑驗證：
    -   [ ] 對和使用者應用程式對接的連線，路徑驗證應被設定成可接受所有合法路徑
    -   [ ] 對需要高度安全性的系統，應被設定成僅接受特定適當的政策的路徑

### User Guidance (Subscribers)

對於和 PKI 申請權證的使用者：

-   [ ] 使用者應產生屬於自己的金鑰，用作簽證和身份證明
-   [ ] 使用者可能自己產生金鑰，或從可信任的資源取得金鑰
-   [ ] 使用者應包管好私鑰，包括加密私鑰的 PIN 碼或密碼
-   [ ] 使用者應請求撤銷，當他覺得該模組被偷、複製或破壞
-   使用者應管理舊的金鑰，除非管理單位有另外政策說明：
    -   [ ] 當簽證過期就應把私鑰丟棄
    -   [ ] 2. 用來產生簽章的私鑰，應等到其產生的私鑰都被重新加密或捨棄後才能丟棄
