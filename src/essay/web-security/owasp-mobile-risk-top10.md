# OWASP 行動裝置風險

## 不同平台間的錯誤實作（Improper Platform Usage）

例如把機敏資料存進 local storage 而不是原生的加密儲存空間：

- iOS 的 `Keychain`
- Android 的 `Keystore`

請參照各平台的最佳做法！！

## 不安全的資料儲存（Insecure Data Storage）

可能的儲存空間：

- Log
- SD card
- Cloud synced
- OS
- Frameworkd（框架如：Flutter）
- Binary data（程式碼裡面）

預防：

- 只儲存必要資訊
- 將敏感檔案加密，和選擇好儲存的位置

[iGoat](https://github.com/OWASP/igoat)的[教學影片](https://youtu.be/U3wabqTTXSE?t=589)。

## 傳輸層保護不足（Insecure Communication）

傳輸媒介可包含：

- 網路連線
- Wifi 連線
- 近場通訊（Near Field Communication，NFC）連線
- ...

最佳做法：

- 確保所有敏感性資料有採用加密方式（TLS、SSL）進行傳輸
  - 並實踐其最佳做法
- 持續注意網路流量
- 不要把機敏資料透過 `SMS`、`MMS` 傳出去

## 不安全的驗證機制（Insecure Authentication）

- 把 Session 或 Token 儲存進安全位置
- 別用 PIN 碼驗證
- 若您的 App 無須 **離線存取**，請停用此功能
- 若您的應用程式需維持機密性，請進行 **雙因素身分驗證**
- 善用如 Microsoft / Google Authenticator 等服務

## 錯誤的使用密碼學(Broken Cryptography)

- 保護好你的鑰匙
- 別自己設計密碼學相關的演算法
- 不安全或過時的演算法（不單指加密）
  - RC2
  - MD4
  - MD5
  - SHA1

## 不安全的授權機制（Insecure Authorization）

```
GET /api/some-method?rule=user HTTP/1.1
```

可以輕易改成 `rule=admin`

請用 Server 端的資料來授權使用者

## 你的 APP 寫得不好（Poor Code Quality）

泛指所有在 Client 端的發生的問題

- buffer overflow
- format string vulnerabilities
- ...

預防：

- 讓多人一起檢查程式碼
- 寫好看的程式碼，好看的程式碼幫助 Debug
- `buffer overflow` 和 `memory leak` 是高風險的安全性問題

```c
include <stdio.h>

 int main(int argc, char **argv)
 {
    char buf[8]; // buffer for eight characters
    gets(buf); // 使用者輸入，這很危險！
    printf("%s\n", buf); // print out data stored in buf
    return 0; // 0 as return value
 }
```

## 你的程式碼被放到非正常環境了（Code Tampering）

一般來說，所有 APP 都會有這問題
但是如果 APP 大部分邏輯都在驗證後或 Server 端的輸出，則此類安全性議題可忽略

> 較需要注意的產業：手遊、工具程式

需參照各平台的最佳作法來預防。

## 逆向工程（Reverse Engineering）

有工具可預防（IDA Pro、Hopper），也有很多工具可幫助逆向工程，挑一下

> 減少一個 Function 的工作，讓逆向後的程式碼不容易閱讀

## 可影響程式運行的機制（Extraneous Functionality）

攻擊者可以把 APP 執行在 local 端，然後改設定檔或觀察 log。

- 最終的程式碼不能有 `debug` 的 log
- 避免若 config 檔變化了，產品的機敏資訊或特殊環境仍能運行或暴露
  - 單元或整合測試不要在最終產品中
  - 不能有 UAT、staging、demo 或 test 環境的程式碼在最終產品

## 舊的

### 伺服器端安全控制脆弱（Weak Server Side Controls）

後端需要注意可能遭受的攻擊：

- [OWASP Top 10](/ZR-UNvOeRjCGIRVNJMVXpw)
- [OWASP API Top 10](/C_BB9B5fQwyODuOZbfCmXg)

基本觀念：

- 絕不相信用戶端
- 謹慎設計行動裝置的伺服器端控制
- 絕不使用用戶端應用程式執行存取控制

### 非故意或意外造成的資料外洩（Unintended Data Leakage）

- 將裝置可收集的資料限制在其所需的範圍
- 切勿將敏感資料儲存於公共場所
- 瞭解並密切監控您的應用程式處理，如：剪下 - 貼上、應用程式背景處理、Cookie、 URL 快取及鍵盤按下快取等動作

### 客戶端注入(Client Side Injection)

- 使用白名單方法是抵擋 XSS
- 確保使用者資料通過參數化的查詢
- 驗證並編碼所有儲存在裝置上的資料

使用嚴謹的身分驗證與授權（例如：雙因素認證）

### 不適當的 Session 處理（Improper Session Handling）

- 避免使用裝置的硬體識別碼來當作 Session 值
- Session 值的過期時間應設定在一個可接受範圍內
- 應有能夠快速撤銷 Token 的機制

### 安全決策是經由不受信任的輸入（Security Decisions Via Untrusted Inputs）

假設 Skype 應用程式具有 `HTML` 或 `Script Injection` 弱點，攻擊者只要事先把具有惡意連結的 `iframe` 寫入某個特定網頁：

```
<iframe src="skype:17031234567?call"></iframe>
```

一但可攜式行動裝置的瀏覽器讀取到此 `iframe` 程式碼時，Skype 應用程式將無需使用者授權，自動開始播號給指定的電話號碼。

**Cross Site Rrequest Foriegn**

### 封裝檔案保護不足 / 缺少二進位保護（Lack of Binary Protections）

Binary 保護可確保攻擊者無法透過逆向工程獲得您的 App

- 切勿將程式碼儲存在不受您控制的不安全環境下
- 確保正確使用憑證綁定及偵錯工具偵測控制
- 監控執行階段程式碼是否在 App 活動中出現異常

### 側通道資料洩漏（Side Channel Data Leakage）

資料應避免自動儲存於可攜式行動裝置內

- 網頁暫存（Web Cache）
- 按鍵側錄（Keystorke Logging）
- 擷取畫面（Screenshots）
- 日誌檔（Logs）
- 暫存目錄（Temp Directories）

### 敏感資訊洩漏（Sensitive Informaiton Disclosure）

應用程式原始碼中，把輸入或輸出的相關參數直接寫入在程式碼當中
