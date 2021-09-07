# OWASP 驗證機制最佳指南

## Passsword

Referer: https://github.com/OWASP/owasp-mstg/blob/master/Document/0x04e-Testing-Authentication-and-Session-Management.md#testing-best-practices-for-passwords-mstg-auth-5-and-mstg-auth-6

- [架構的檢查](https://github.com/OWASP/CheatSheetSeries/blob/master/cheatsheets/Authentication_Cheat_Sheet.md#implement-proper-password-strength-controls)
- 檢查密碼強度，[zxcvbn](https://github.com/dropbox/zxcvbn)
- 檢查密碼被破解過，[Have I been pwned?](https://haveibeenpwned.com/)
- 限制嘗試
- 自己攻擊看看，[Burp Suite Intruder](https://portswigger.net/burp/help/intruder_using.html)

## Session

Referer: https://github.com/OWASP/owasp-mstg/blob/master/Document/0x04e-Testing-Authentication-and-Session-Management.md#session-management-best-practices

- 每次需要驗證身份時要做檢查
- 要過期
- 根據不同 Framework 有不同 best practice，請詳閱！！

## 2FA

- SMS-OTP
  - NIST: "Due to the risk that SMS messages may be intercepted or redirected, implementers of new systems SHOULD carefully consider alternative authenticators."
  - 可能遭遇的威脅和預防方式：https://github.com/OWASP/owasp-mstg/blob/master/Document/0x04e-Testing-Authentication-and-Session-Management.md#dangers-of-sms-otp
- Transaction Signing with Push Notifications and PKI
  - 手機建立公私鑰
  - 公鑰送給後端
  - 若需要驗證的行為：
    - 發通知（Push notifications）到手機
    - 使用者授權
    - 傳送私鑰簽核過的訊息
    - 驗證
  - 詳細注意事項和測試：https://github.com/OWASP/owasp-mstg/blob/master/Document/0x04e-Testing-Authentication-and-Session-Management.md#transaction-signing-with-push-notifications-and-pki

## JWT

- 每次都要驗證
- 鑰匙藏好
- 藏好機敏資料，若有必要請加密
- 使用 `jti`（JWT ID）
- token 請放在 `KeyChain` 或 `KeyStore`
- Header 不能讓 `alg` 可接受 `none`
- `exp` 要注意

## OAuth 2.0

- 別用 `implicit grant`，`code grant` 要一次性且短時
- PKCE
- Access Token 若存在不信任的地方要短暫的期限
- 有限制的 `scope`
- 除了 access token 要有可以驗證使用者的資訊
- [OAuth 2.0 for Native APP](https://tools.ietf.org/html/draft-ietf-oauth-native-apps-12)

## 怎麼確認這是同一台手機

如論何種狀況，你都應該驗證請求是否來自不同裝置。因此，要能確認你的程式真的被裝在正確的裝置上。

iOS：

> In iOS, a developer can use `identifierForVendor`, which is related to the bundle ID: the moment you change a bundle ID, the method will return a different value. When the app is ran for the first time, make sure you store the value returned by `identifierForVendor` to the KeyChain, so that changes to it can be detected at an early stage.

Android：

> In Android, the developer can use `Settings.Secure.ANDROID_ID` till Android 8.0 (API level 26) to identify an application instance. Note that starting at Android 8.0 (API level 26), `ANDROID_ID` is no longer a device unique ID. Instead, it becomes scoped by the combination of app signing key, user and device. So validating `ANDROID_ID` for device blocking could be tricky for these Android versions. Because if an app changes its signing key, the `ANDROID_ID` will change and it won't be able to recognize old users devices. Therefore, it's better to store the `ANDROID_ID`encrypted and privately in a private a shared preferences file using a randomly generated key from the `AndroidKeyStore` and preferably AES_GCM encryption. The moment the app signature changes, the application can check for a delta and register the new `ANDROID_ID`. The moment this new ID changes without a new application signing key, it should indicate that something else is wrong.

除此之外，在一開始的裝置綁定上，可以透過簽發請求，來提高安全性。

> Next, the device binding can be extended by signing requests with a key stored in the `Keychain` for iOS and in the `KeyStore` in Android can reassure strong device binding.

你也可以驗證 `IP`、`地理位置`和`時間軌跡`。

## 其他

- 讓使用者知道 {} 也登入帳號了
  - 哪個裝置
  - 哪個時間
  - 哪個地點
- 要通知使用者有新的登入
- 讓使用者知道最後行為是什麼
- 每次登入、登出要做紀錄
- 這些是機敏的行為
  - 登入
  - 改密碼
  - 個資改變 (name, email address, telephone number, etc.)
  - 敏感行為 (purchase, accessing important resources, etc.)
  - 同意條款
